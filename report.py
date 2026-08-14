import csv
import random

def format_equity(equities):
    formatted_equities = {label: equity['wins'] + (equity['ties'] / 2) for label, equity in equities.items()}
    return formatted_equities

def render_grid():
    from simulate import hand_in_label, hand_equity, create_hole_from_label
    from cards import make_deck
    deck = make_deck()
    rng = random.Random(42)
    trials = 100
    labels = hand_in_label(deck)
    equities = {label: hand_equity(create_hole_from_label(label), trials, rng) for label in labels}
    formatted_equities = format_equity(equities)

    with open('equity_grid.csv', 'w', newline='') as csvfile:
        fieldnames = ['Hand', 'Equity']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for label, equity in formatted_equities.items():
            writer.writerow({'Hand': label, 'Equity': equity})



def plot_heatmap():
    import matplotlib.pyplot as plt
    import seaborn as sns
    import pandas as pd

    def prepare_matrix_from_csv(path='equity_grid.csv'):
        df = pd.read_csv(path)
        ranks = ['A','K','Q','J','T','9','8','7','6','5','4','3','2']
        mat = pd.DataFrame(index=ranks, columns=ranks, data=float('nan'))

        equity_map = {row['Hand']: row['Equity'] for _, row in df.iterrows()}

        for i, r in enumerate(ranks):
            for j, c in enumerate(ranks):
                if r == c:
                    label = r + r
                else:
                    # convention: suited when row rank > col rank (below diagonal), offsuit otherwise
                    label = r + c + ('s' if i > j else 'o')

                if label in equity_map:
                    mat.at[r, c] = equity_map[label]
                else:
                    # try reversed label (some CSVs may use order-independent labels)
                    rev = c + r + ('s' if j > i else 'o') if r != c else label
                    mat.at[r, c] = equity_map.get(rev, float('nan'))

        return mat

    pivot_table = prepare_matrix_from_csv('equity_grid.csv')

    sns.heatmap(pivot_table, annot=True, fmt=".2f", cmap="coolwarm", cbar_kws={'label': 'Equity'})
    plt.title('Poker Hand Equity Heatmap')
    plt.tight_layout()
    plt.show()

if __name__ == '__main__':
    render_grid()
    plot_heatmap()
