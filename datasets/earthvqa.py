"""
datasets/earthvqa.py

Dataset adapter for EarthVQA.
This adapter converts EarthVQA image-question-answer data into the
same standardized sample format used by the proposed evaluation framework.
"""

import json
from pathlib import Path

from datasets.base import BaseDataset


class EarthVQADataset(BaseDataset):
    """
    Dataset adapter for EarthVQA.

    Expected EarthVQA-style structure:
        qa_path: JSON file containing image-question-answer pairs
        image_dir: folder containing the images
        mask_dir: optional folder containing segmentation masks
    """

    def __init__(
        self,
        data_root: str,
        subset: str = "default",
        qa_path: str | None = None,
        image_dir: str | None = None,
        mask_dir: str | None = None,
    ):
        super().__init__(data_root=data_root, subset=subset)

        self.data_root = Path(data_root)
        self.qa_path = Path(qa_path) if qa_path else self.data_root / "qa.json"
        self.image_dir = Path(image_dir) if image_dir else self.data_root / "images"
        self.mask_dir = Path(mask_dir) if mask_dir else None

    def load(self) -> list[dict]:
        """
        Load EarthVQA QA pairs and return standardized samples.
        """
        if not self.qa_path.exists():
            raise FileNotFoundError(
                f"Could not find EarthVQA QA file: {self.qa_path}"
            )

        with open(self.qa_path, "r", encoding="utf-8") as file:
            qa_data = json.load(file)

        self._samples = []
        sample_index = 0

        for image_name, qa_list in qa_data.items():
            if not isinstance(qa_list, list):
                continue

            for qa_item in qa_list:
                question_type, question, answer = self._parse_qa_item(qa_item)

                sample = {
                    "id": f"earthvqa_{sample_index}",
                    "dataset": "EarthVQA",
                    "subset": self.subset,
                    "task": self._map_question_type(question_type),
                    "image_paths": [str(self.image_dir / image_name)],
                    "question": question,
                    "answer": answer,
                    "metadata": {
                        "question_type": question_type,
                        "image_name": image_name,
                    },
                    "raw": qa_item,
                }

                if self.mask_dir is not None:
                    sample["metadata"]["mask_path"] = str(self.mask_dir / image_name)

                self._samples.append(sample)
                sample_index += 1

        return self._samples

    def _parse_qa_item(self, qa_item: dict) -> tuple[str, str, str]:
        """
        Extract question type, question, and answer from one EarthVQA QA item.
        Supports common field name variations.
        """
        question_type = (
            qa_item.get("questype")
            or qa_item.get("question_type")
            or qa_item.get("type")
            or "unknown"
        )

        question = (
            qa_item.get("question")
            or qa_item.get("ques")
            or qa_item.get("prompt")
            or ""
        )

        answer = (
            qa_item.get("answer")
            or qa_item.get("ans")
            or qa_item.get("label")
            or ""
        )

        return question_type, question, answer

    def _map_question_type(self, question_type: str | None = None) -> str:
        """
        Map EarthVQA question types to broad task types.
        """
        if question_type is None:
            return "vqa"

        question_type_lower = question_type.lower()

        if "counting" in question_type_lower:
            return "counting"

        if "judging" in question_type_lower:
            return "vqa"

        if "analysis" in question_type_lower:
            return "reasoning"

        if "situation" in question_type_lower:
            return "reasoning"

        return "vqa"

    def get_task_type(self) -> str:
        """
        Return the default task type for EarthVQA.
        """
        return "vqa"

    def get_dataset_name(self) -> str:
        """
        Return dataset name.
        """
        return "EarthVQA"