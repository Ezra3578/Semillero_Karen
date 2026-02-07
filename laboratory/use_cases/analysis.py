from laboratory.domain.sample import Sample

def analyze_sample_uc(*, sample: Sample,
                      fq: dict | None = None,
                      micro: dict | None = None,):
    sample.add_results(
        fq=fq,
        micro=micro,
    )
