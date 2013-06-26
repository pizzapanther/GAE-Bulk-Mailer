
class ApiException (Exception):
  pass

class ParameterRequired (Exception):
  def __init__ (self, *args, **kwargs):
    args = list(args)
    args[0] = 'API parameter required: ' + args[0]
    super(ParameterRequired, self).__init__(*args, **kwargs)
    