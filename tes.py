if __name__ == "__main__":
    unassigned = [[[1, 2] for y in range(9)] for x in range(9)]  # 9 * 9 array of lists
    unassignedVars = [list([list(innerlist) for innerlist in outerlist]) for outerlist in unassigned]
    unassignedVars.append([[9]])
    unassignedVarsCopy = [list([list(innerlist) for innerlist in outerlist]) for outerlist in unassignedVars]
    print unassigned
    print unassignedVars
    print unassignedVarsCopy
    print unassignedVarsCopy[9][0][0]