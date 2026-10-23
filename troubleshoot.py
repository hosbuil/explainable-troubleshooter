"""AI-generated educational rule engine. No system changes or network calls."""
import argparse
import json
from pathlib import Path

QUESTIONS = {
    'power': 'Does the device turn on?',
    'wifi': 'Is the device connected to Wi-Fi?',
    'internet_ip': 'Can a known internet IP be reached?',
    'dns': 'Does a domain name resolve?',
    'other_sites': 'Do other websites work?',
    'disk_full': 'Is the disk almost full?',
}
RULES = [
    ('power', {'power': False}, 'Power check', 'Check the outlet, charger and cable before investigating software.'),
    ('wifi', {'power': True, 'wifi': False}, 'Local connection check', 'Confirm Wi-Fi is enabled and the intended network is selected.'),
    ('upstream', {'power': True, 'wifi': True, 'internet_ip': False}, 'Network path check', 'Compare another device on the same network; a router or upstream outage is possible.'),
    ('dns', {'power': True, 'wifi': True, 'internet_ip': True, 'dns': False}, 'DNS check', 'Compare name resolution on another device. Working IP access with failed names suggests a DNS issue.'),
    ('site', {'power': True, 'wifi': True, 'internet_ip': True, 'dns': True, 'other_sites': True}, 'Site-specific check', 'If the target site fails while other sites work, check its status and the browser error.'),
    ('disk', {'power': True, 'disk_full': True}, 'Storage check', 'Review storage usage and back up files before choosing what to remove.'),
]

def diagnose(answers):
    if not isinstance(answers, dict):
        raise ValueError('Answers must be a JSON object.')
    unknown = set(answers) - set(QUESTIONS)
    if unknown:
        raise ValueError('Unknown question keys: ' + ', '.join(sorted(unknown)))
    if any(value is not None and type(value) is not bool for value in answers.values()):
        raise ValueError('Each answer must be true, false or null (unknown).')
    matches, pending = [], []
    for rule_id, conditions, title, advice in RULES:
        contradicted = any(answers.get(key) is not None and answers[key] != expected
                           for key, expected in conditions.items())
        if contradicted:
            continue
        missing = [key for key in conditions if answers.get(key) is None]
        if missing:
            pending.append({'rule': rule_id, 'needs': missing})
        else:
            matches.append({'rule': rule_id, 'title': title, 'advice': advice,
                            'evidence': conditions})
    return {'recommendations': matches, 'pending_rules': pending,
            'unanswered': [key for key in QUESTIONS if answers.get(key) is None],
            'status': 'recommendations' if matches else 'insufficient_evidence' if pending else 'no_matching_rule'}

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input', type=Path, help='JSON answers; omit for an interactive session')
    args = parser.parse_args()
    try:
        if args.input:
            answers = json.loads(args.input.read_text(encoding='utf-8'))
        else:
            answers = {}
            for key, question in QUESTIONS.items():
                while True:
                    value = input(question + ' [y/n/?] ').strip().lower()
                    if value in ('y', 'n', '?'):
                        answers[key] = {'y': True, 'n': False, '?': None}[value]
                        break
                    print('Enter y, n or ?.')
        print(json.dumps(diagnose(answers), indent=2))
    except (ValueError, OSError, EOFError) as exc:
        parser.exit(2, f'Input error: {exc}\n')

if __name__ == '__main__':
    main()
