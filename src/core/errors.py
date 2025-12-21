class AudioEngineError(Exception):
    pass

class ResourceNotFoundError(AudioEngineError):
    pass

class ConfigValidationError(AudioEngineError):
    pass