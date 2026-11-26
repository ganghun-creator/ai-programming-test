import pytest

from load_scores import load_scores


def test_유효한_점수와_헤더만_있는_파일을_읽는다(tmp_path):
    file = tmp_path / "scores.csv"
    file.write_text("이름,점수\n김하나,88\n이둘,0\n삼셋,100\n", encoding="utf-8")

    kept, skipped = load_scores(file)

    assert kept == [("김하나", 88), ("이둘", 0), ("삼셋", 100)]
    assert skipped == []


def test_파일이_없으면_FileNotFoundError를_발생시킨다(tmp_path):
    with pytest.raises(FileNotFoundError):
        load_scores(tmp_path / "missing.csv")


def test_헤더만_있으면_빈_결과를_반환한다(tmp_path):
    file = tmp_path / "header_only.csv"
    file.write_text("이름,점수\n", encoding="utf-8")

    assert load_scores(file) == ([], [])


@pytest.mark.parametrize(
    ("row", "reason"),
    [
        ("하나,90,추가", "열"),
        ("둘,", "점수"),
        ("셋,abc", "점수"),
        ("넷,-1", "점수"),
        ("다섯,101", "점수"),
        (",90", "이름"),
    ],
)
def test_잘못된_행은_kept에서_제외하고_skipped에_기록한다(
    tmp_path, row, reason
):
    file = tmp_path / "invalid.csv"
    file.write_text(f"이름,점수\n{row}\n", encoding="utf-8")

    kept, skipped = load_scores(file)

    assert kept == []
    assert len(skipped) == 1
    line_no, original, skip_reason = skipped[0]
    assert line_no == 2
    assert original == row
    assert reason in skip_reason


def test_중복된_이름은_모두_kept에_남긴다(tmp_path):
    file = tmp_path / "duplicates.csv"
    file.write_text("이름,점수\n김하나,88\n김하나,95\n", encoding="utf-8")

    kept, skipped = load_scores(file)

    assert kept == [("김하나", 88), ("김하나", 95)]
    assert skipped == []


def test_빈_줄은_skipped에_기록하지_않는다(tmp_path):
    file = tmp_path / "blank_line.csv"
    file.write_text("이름,점수\n\n김하나,88\n", encoding="utf-8")

    kept, skipped = load_scores(file)

    assert kept == [("김하나", 88)]
    assert skipped == []