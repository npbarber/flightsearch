import os

def prepend(env_var, value):
    curr_val = os.environ.get(env_var, '')
    if curr_val:
        value += ':%s' % curr_val
    os.environ[env_var] = value



repo_root = os.path.dirname(__file__)
prepend('PATH', '%s/bin' % repo_root)
prepend('PYTHONPATH', repo_root)
