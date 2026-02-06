from laboratory.use_cases.register_sample import register_sample
from laboratory.repository import load_samples, save_samples


class Laboratory:
    def register_sample(self, data: dict):
        samples = load_samples()

        existing_codes = [
            s.get("Código") or s.get("codigo")
            for s in samples
            if s.get("Código") or s.get("codigo")
        ]

        sample = register_sample(
            data=data,
            existing_codes=existing_codes,
        )

        samples.append(sample.to_dict())
        save_samples(samples)

        return sample
