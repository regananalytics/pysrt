// See https://aka.ms/new-console-template for more information
using NetMQ;
using NetMQ.Sockets;
using MemCore;
using System.Diagnostics;
using System.Text.Json;

string gameName = "re2";
string gameConf = @"C:/Users/verti/Documents/GitHub/pysrt/memconf/" + gameName + ".yaml";

// Parse the config
var memConfParser = new MemConfigParser();
memConfParser.Parse(gameConf);

// Load the process
var process = Process.GetProcessesByName(gameName)?.FirstOrDefault();
if (process == null)
    throw new System.Exception("Process not found");

// Build Config
memConfParser.Build("RE2_WW_20211217_1", process);


// Start the publisher
using (var pubSocket = new PublisherSocket())
{
    pubSocket.Options.SendHighWatermark = 1000;
    pubSocket.Bind("tcp://*:5556");

    while (true)
    {
        var dict = new Dictionary<string, object?>();

        // Get State Values
        foreach (var state in memConfParser.States)
        {
            state.Value.Update();
            dict.Add( state.Key, state.Value.Deref());
        }

        // Get StateStruct Values
        foreach (var stateStruct in memConfParser.Structs)
        {
            stateStruct.Value.Update();
            dict.Add(stateStruct.Key, stateStruct.Value.Deref());
        }

        // Publish the values
        string json = JsonSerializer.Serialize(dict);
        pubSocket.SendFrame(json);
        Console.WriteLine(json);

        // Sleep
        Thread.Sleep(2000);
    }
}
