"""
datasets/disasterm3.py

Dataset adapter for the DisasterM3 benchmark.
This file separates DisasterM3-specific loading logic from the main
evaluation script and converts raw samples into a common format.
"""

import json
from pathlib import Path

from datasets.base import BaseDataset


class DisasterM3Dataset(BaseDataset):
    """
    Dataset adapter for DisasterM3.

    Expected folder structure:

        data/
        ├── bearing_body.json
        ├── caption.json
        ├── recovery.json
        └── images/

    Example:
        dataset = DisasterM3Dataset(data_root="data", subset="bearing_body")
        samples = dataset.load()
    """

    def load(self) -> list[dict]:
        """
        Load a DisasterM3 subset JSON file and return standardized samples.

        Returns:
            list[dict]: List of standardized samples.
        """
        data_root = Path(self.data_root)
        subset_file = data_root / f"{self.subset}.json"
        image_root = data_root / "images"

        if not subset_file.exists():
            raise FileNotFoundError(
                f"Could not find DisasterM3 subset file: {subset_file}"
            )

        with open(subset_file, "r", encoding="utf-8") as file:
            raw_data = json.load(file)

        self._samples = []

        for index, item in enumerate(raw_data):
            sample_id = item.get("id", f"{self.subset}_{index}")
            image_paths = self._extract_image_paths(item, data_root, image_root)

            sample = {
                "id": sample_id,
                "dataset": "DisasterM3",
                "subset": self.subset,
                "task": self.get_task_type(),
                "image_paths": image_paths,
                "question": item.get("prompts"),
                "options": item.get("options_str") or item.get("option_str"),
                "answer": item.get("answer"),
                "raw": item,
            }

            self._samples.append(sample)

        return self._samples

    def _extract_image_paths(
        self, item: dict, data_root: Path, image_root: Path
    ) -> list[str]:
        """
        Extract image paths from one DisasterM3 sample.

        Some DisasterM3 tasks use pre- and post-disaster images.
        Other tasks may use a single image.
        """
        image_paths = []

        if "pre_image_path" in item:
            image_paths.append(str(image_root / item["pre_image_path"]))

        if "post_image_path" in item:
            image_paths.append(str(image_root / item["post_image_path"]))

        if "image_path" in item:
            normalized_path = item["image_path"].replace("\\", "/")
            image_paths.append(str(data_root / normalized_path))

        return image_paths

    def get_task_type(self) -> str:
        """
        Map DisasterM3 subsets to broad task types.
        """
        subset_to_task = {
            "bearing_body": "vqa",
            "building_damage_counting": "counting",
            "road_damage_counting": "counting",
            "disaster_type": "classification",
            "landuse": "classification",
            "relational_reasoning_qa": "vqa",
            "caption": "captioning",
            "recovery": "report_generation",
        }

        return subset_to_task.get(self.subset, "unknown")

    def get_dataset_name(self) -> str:
        """
        Return the dataset name.
        """
        return "DisasterM3"