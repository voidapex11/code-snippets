elements.foam_bomb = {
    color: "#34599e",
    behavior: [
        "XX|EX:10>foam|XX",
        "XX|XX|XX",
        "M2|M1 AND EX:10>foam|M2",
    ],
    category: "weapons",
    state: "solid",
    density: 1300,
    tempHigh: 1455.5,
    stateHigh: "molten_steel",
    excludeRandom: true,
    cooldown: defaultCooldown
}