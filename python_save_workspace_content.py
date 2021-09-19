#pip install dill --user

import dill          
filename = 'globalsave.pkl'
dill.dump_session(filename)

# and to load the session again:
dill.load_session(filename)
