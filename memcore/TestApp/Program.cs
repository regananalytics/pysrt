// See https://aka.ms/new-console-template for more information
using NetMQ;
using NetMQ.Sockets;
using MemCore;
using System.Diagnostics;
using System.Reflection;
using System.Text.Json.Serialization;
using System.Text.Json;

string gameName = "re2";
string gameConf = @"C:/Users/verti/Documents/GitHub/pysrt/memconf/" + gameName + ".yaml";


// Load the process
// var process = Process.GetProcessesByName(gameName)?.FirstOrDefault();

// Parse the config
var memConf = new MemConfig();
memConf.Parse(gameConf);
memConf.Build("RE2_WW_20220613_1");

//if (memConf.Pointers != null)
//{
//    foreach (var mem_pnt in memConf.Pointers)
//        mem_pnt.Value.AttachProcess(process);
//}

using (var pubSocket = new PublisherSocket())
{
    pubSocket.Options.SendHighWatermark = 1000;
    pubSocket.Bind("tcp://*:5556");

    int value = 0;
    while (true)
    {
        var dict = new Dictionary<string, string>();

        foreach (var mem_pnt in memConf.Pointers)
        {
            var name = mem_pnt.Key;
            //var pointer = mem_pnt.Value;
            //string value = (string) pointer.Deref();
            
            dict[name] = (value++).ToString();
        }

        string json = JsonSerializer.Serialize(dict);
        pubSocket.SendFrame(json);
        Console.WriteLine(json);

        Thread.Sleep(1000);
    }
}

