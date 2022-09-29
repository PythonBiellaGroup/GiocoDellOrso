import argparse
import pickle


parser = argparse.ArgumentParser()
parser.add_argument('-i', '--input', help='input file', required=True)
parser.add_argument(
    '-d', '--dump',
    type=bool,
    help='dump the state', default=False
)
parser.add_argument(
    '--reverse',
    type=bool,
    help='reverse the input file',
    default=False
)
parser.add_argument('--state', help='display valueof the state', default='')

args = parser.parse_args()
input = args.input
state = args.state
with open(input, 'rb') as f:
    data: dict[str, float] = pickle.load(f)

    states = data['states_value'].copy()
    data['states_value'] = None

    print(data)
    if state == '' and args.dump:
        states = {
            k: v for k, v in sorted(
                states.items(), key=lambda item: item[1],
                reverse=args.reverse
            )
        }
        for key, value in states.items():
            print(key, value)
    else:
        print("the value of the state is:")
        print(f"{state}: {data[state]}")
