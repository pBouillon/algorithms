using System;
using System.Collections.Generic;

namespace TabuSearch
{
    class Program
    {
        static Dictionary<int, int[]> GetInitialState(int procs, int[] tasks)
        {
            if (procs < 1)
            {
                Console.Error.WriteLine("Must provide at least one processor");
                Environment.Exit(1);
            }

            var s0 = new Dictionary<int, int[]> { [0] = tasks };
            for (var i = 1; i < procs; ++i) s0[i] = new int[0];

            return s0;
        }

        static List<Dictionary<int, int[]>> GetNeighbors(Dictionary<int, int[]> state)
        {
            var neighbors = new List<Dictionary<int, int[]>>();

            for (var source = 0; source < state.Count; ++source)
            {
                for (var taskId = 0; taskId < state[source].Length; ++taskId)
                {
                    for (var destination = 0; destination < state.Count; ++destination)
                    {
                        if (source == destination) continue;

                        // creating new state
                        var newNeighbor = new Dictionary<int, int[]>(state);
                        int toSwap = state[source][taskId];
                        var newState = new List<int>();

                        // creating new source element
                        for (var i = 0; i < newNeighbor[source].Length; ++i)
                        {
                            if (i == taskId) continue;
                            newState.Add(newNeighbor[source][i]);
                        }

                        newNeighbor[source] = newState.ToArray();
                        newState.Clear();

                        // creating new destination element
                        foreach (var i in newNeighbor[destination]) newState.Add(i);
                        newState.Add(toSwap);

                        newNeighbor[destination] = newState.ToArray();

                        // appending new state
                        neighbors.Add(newNeighbor);
                    }
                }
            }

            return neighbors;
        }

        static void Main(string[] args)
        {
            Console.WriteLine("Hello World!");
        }
    }
}
