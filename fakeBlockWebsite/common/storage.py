from whitenoise.storage import CompressedManifestStaticFilesStorage


class WhiteNoiseStaticFilesStorage(CompressedManifestStaticFilesStorage):
	"""
	Change the value of the manifest_strict field of the whitenoise storage
	class to avoid missing manifest error.
	"""
	manifest_strict = False