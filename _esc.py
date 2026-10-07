# -*- coding: utf-8 -*-
import io, re, collections
css = io.open("transicion.css", encoding="utf-8").read()
# split scene blocks
parts = re.split(r"(?m)^/\* =+ ", css)
prop = re.compile(r"\{([^{}]*)\}")
rep = 0
tot = 0
ejemplos = []
for p in parts[1:]:
    nm = re.findall(r"@keyframes\s+([\w-]+)", p)
    if not nm:
        continue
    tot += 1
    vistos = {}
    for kf in re.finditer(r"@keyframes\s+([\w-]+)\s*\{((?:[^{}]|\{[^{}]*\})*)\}", p):
        name = kf.group(1)
        props = set()
        for decl in re.finditer(r"(?:^|[;{\s])([-a-zA-Z]+)\s*:", kf.group(2)):
            props.add(decl.group(1).lower())
        for pr in props:
            if pr in vistos and vistos[pr] != name:
                rep += 1
                ejemplos.append((p.splitlines()[0][:50], pr, vistos[pr], name))
                break
            vistos[pr] = name
print("escenas con keyframes:", tot, " con propiedad repetida entre keyframes:", rep)
for e in ejemplos[:8]:
    print("  ", e)
# ::after presence
print("escenas con ::after:", len(re.findall(r"^\.tema-[\w-]+::after", css, re.M)))
print("escenas con .tema- {:", len(re.findall(r"^\.tema-[\w-]+ \{", css, re.M)))
# base .escena::after
i = css.find(".escena::after")
print("base .escena::after:", i, repr(css[i-100:i+200]) if i>0 else "")
