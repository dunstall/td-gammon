# TD-Gammon
Implementation of TD-Gammon with Keras/Tensorflow.

## Getting Started

### Installation
1. Clone the repo
```bash
  git clone https://github.com/dunstall/td-gammon.git
```
2. Create a virtual environment (optional)
```bash
  python3 -m venv td-gammon-env
  source td-gammon-env/bin/activate
```

3. Install PIP packages
```bash
  pip3 install -r requirements.txt
```

### Usage
```
usage: main.py [-h] [--test] [--debug] [--restore RESTORE]

TD-Gammon model.

optional arguments:
  -h, --help         show this help message and exit
  --test             test model
  --debug            debug logging
  --restore RESTORE  path to the model to restore from
```

#### Training
```bash
  python3 main.py
```

#### Testing
```bash
  python3 main.py --test
```

#### Restore Saved Model
```bash
  python3 main.py --restore checkpoints/mymodel
```

## Resources
* [TD-Gammon Paper](https://pdfs.semanticscholar.org/917e/e68192527f0722fac966163f26b7a4e8e5f3.pdf?_ga=2.138006640.1591278561.1609908105-703813112.1609908105)
* Reinforcement Learning: An Introduction Second Edition (Sutton, Barto)
* [Practical Issues in Temporal Difference Learning](https://papers.nips.cc/paper/1991/file/68ce199ec2c5517597ce0a4d89620f55-Paper.pdf)
