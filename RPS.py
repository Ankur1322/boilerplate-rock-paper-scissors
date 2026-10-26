BEAT = {"R": "P", "P": "S", "S": "R"}
CYCLE = ["R", "R", "P", "P", "S"]
NAMES = ["quincy", "kris", "mrugesh", "abbey"]


def player(prev_play, st={}):
    if prev_play == "" or not st:
        st.clear()
        st.update(me=[], pairs={a + b: 0 for a in "RPS" for b in "RPS"},
                  score=dict.fromkeys(NAMES, 0.0), guess={})
    me = st["me"]
    if prev_play:
        for n, g in st["guess"].items():
            if prev_play in g:
                st["score"][n] += 1.0 / len(g)

    # what the bots see as my history ("" at the start)
    last = me[-1] if me else "R"
    window = me[-10:] if me else [""]
    counts = {x: window.count(x) for x in "RPS"}
    top = max(counts.values())

    if me:
        top_moves = [x for x in "RPS" if counts[x] == top]
        mrugesh = [BEAT[x] for x in top_moves]
    else:
        mrugesh = ["R"]

    pc = {x: st["pairs"][last + x] for x in "RPS"}
    best = max(pc.values())
    abbey = [BEAT[x] for x in "RPS" if pc[x] == best][:1]

    st["guess"] = {
        "quincy": [CYCLE[(len(me) + 1) % 5]],
        "kris": [BEAT[last]],
        "mrugesh": mrugesh,
        "abbey": abbey,
    }
    chosen = max(NAMES, key=lambda n: st["score"][n])
    poss = st["guess"][chosen]

    def value(m):
        return sum((BEAT[b] == m) - (BEAT[m] == b) for b in poss)

    move = max("RPS", key=value)
    if me:
        st["pairs"][last + move] += 1
    me.append(move)
    return move