import vlab
import optuna

xfoil = vlab.Xfoil()

def objective(trial: optuna.Trial):
    s,p = [],[]
    for i in range(8):
        s.append(trial.suggest_uniform("s"+str(i), -0.05, 0.2))
        p.append(trial.suggest_uniform("p"+str(i), -0.2, 0.05))
    a = trial.suggest_uniform("a", -5, 10)
    cd,cl = xfoil.cd_cl(vlab.nurbs(s,p), a)
    if cd is None or cl is None:
        cl,cd=0,1
    return -cl/cd #(cd+1)*(abs(cl-0.6)+1)

sampler = optuna.samplers.CmaEsSampler()
study = optuna.create_study(sampler=sampler)
study.optimize(objective, n_trials=250000)
xfoil.stop()
