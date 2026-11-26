
import pytest
from load_scores import load_scores


def test_정상_파일을_읽는다(tmp_path):
    file = tmp_path / "normal.csv"
    file.write_text(
        "이름,점수\n김하나,88\n이둘,95\n",
        encoding="utf-8"
    )

    kept, skipped = load_scores(file)

    assert kept == [("김하나", 88), ("이둘", 95)]
    assert skipped == []


def test_없는_파일이면_오류가_난다(tmp_path):
    file = tmp_path / "없는파일.csv"

    with pytest.raises(FileNotFoundError):
        load_scores(file)


def test_헤더만_있으면_빈_결과를_반환한다(tmp_path):
    file = tmp_path / "empty.csv"
    file.write_text("이름,점수\n", encoding="utf-8")

    kept, skipped = load_scores(file)

    assert kept == []
    assert skipped == []


def test_열_개수가_다르면_건너뛴다(tmp_path):
    file = tmp_path / "columns.csv"
    file.write_text(
        "이름,점수\n김하나,88,추가\n",
        encoding="utf-8"
    )

    kept, skipped = load_scores(file)

    assert kept == []
    assert len(skipped) == 1


def test_점수가_비어있으면_건너뛴다(tmp_path):
    file = tmp_path / "empty_score.csv"
    file.write_text("이름,점수\n김하나,\n", encoding="utf-8")

    kept, skipped = load_scores(file)

    assert kept == []
    assert len(skipped) == 1


def test_점수가_정수가_아니면_건너뛴다(tmp_path):
    file = tmp_path / "not_integer.csv"
    file.write_text("이름,점수\n김하나,abc\n", encoding="utf-8")

    kept, skipped = load_scores(file)

    assert kept == []
    assert len(skipped) == 1


@pytest.mark.parametrize("score, valid", [
    (-1, False),
    (0, True),
    (1, True),
    (99, True),
    (100, True),
    (101, False),
])
def test_점수_경계값(tmp_path, score, valid):
    file = tmp_path / "boundary.csv"
    file.write_text(
        f"이름,점수\n김하나,{score}\n",
        encoding="utf-8"
    )

    kept, skipped = load_scores(file)

    assert (len(kept) == 1) == valid


def test_이름이_비어있으면_건너뛴다(tmp_path):
    file = tmp_path / "empty_name.csv"
    file.write_text("이름,점수\n,88\n", encoding="utf-8")

    kept, skipped = load_scores(file)

    assert kept == []
    assert len(skipped) == 1


def test_동명이인은_모두_남긴다(tmp_path):
    file = tmp_path / "duplicate.csv"
    file.write_text(
        "이름,점수\n김하나,88\n김하나,95\n",
        encoding="utf-8"
    )

    kept, skipped = load_scores(file)

    assert kept == [("김하나", 88), ("김하나", 95)]
    assert skipped == []
