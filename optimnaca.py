import utils
import optuna

def objective(trial: optuna.Trial):
    m = trial.suggest_uniform("m", 0, 10)
    p = trial.suggest_uniform("p", 0, 10)
    t = trial.suggest_uniform("t", 0, 20)
    a = trial.suggest_uniform("a", -5, 10)
    cd,cl = utils.cd_cl(utils.naca4(m,p,t),a)
    if cd is None or cl is None:
        cl,cd=0,1

    return -cl12 # (cd+1)*(abs(cl-0.6)+1)

sampler = optuna.samplers.CmaEsSampler()
study = optuna.create_study(sampler=sampler)
study.optimize(objective, n_trials=250)
