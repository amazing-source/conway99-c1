"""Apply the forced ten-row resolution to a variable Hoffman boundary."""
from pathlib import Path
import argparse
import json
import time

from hoffman_coexistence_extensions import ExtensionModel,SOURCE,OUT


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--prefix',default='37c3bb63972f')
    ap.add_argument('--free',default='3,4,5,6,7')
    ap.add_argument('--root',type=int,default=10)
    ap.add_argument('--seconds',type=float,default=120)
    ap.add_argument('--workers',type=int,default=4)
    ap.add_argument('--weak',action='store_true',help='Only the ten-row resolution, without distance or central row constraints')
    args=ap.parse_args()
    item=next(x for x in json.loads(SOURCE.read_text())['items'] if x['design']['key'].startswith(args.prefix))
    start=time.monotonic()
    model=ExtensionModel(item['design']['blocks'],list(map(int,args.free.split(','))))
    resolution=model.add_resolution(args.root,not args.weak,not args.weak)
    build_seconds=time.monotonic()-start
    result=model.solve(args.seconds,args.workers)
    result.update(source=item['design']['key'],source_blocks=item['design']['blocks'],
                  resolution=resolution,arguments=vars(args),build_seconds=build_seconds,
                  scope='All Hoffman boundaries with retained incidences fixed, via necessary transported row resolution')
    name='resolution_'+args.prefix+'_'+args.free.replace(',','-')+('_weak' if args.weak else '')+'.json'
    OUT.mkdir(exist_ok=True)
    (OUT/name).write_text(json.dumps(result,indent=2))
    print('RESULT',result['status'],'build',round(build_seconds,3),'solve',round(result['seconds'],3),
          'conflicts',result['conflicts'],flush=True)


if __name__=='__main__':main()
