// See https://aka.ms/new-console-template for more information
using MemCore;
using ProcessMemory;
using System.Diagnostics;
using System.Reflection;
using YamlDotNet.RepresentationModel;

string gameName = "re2";
string gameModel = @"C:/Users/verti/Documents/GitHub/pysrt/models/re2.yaml";
string yaml;

// Load the process
var process = Process.GetProcessesByName(gameName)?.FirstOrDefault();

// Parse the model
using (var reader = new StreamReader(gameModel))
{
    yaml = reader.ReadToEnd();
}
var pointers = MemPointerParser.Parse(yaml);

foreach (var item in pointers)
{
    var name = item.Key;
    var pointer = item.Value;
    pointer.AttachProcess(process);
    Console.WriteLine(name + " " + pointer.Deref()+ "\n");
}


Console.WriteLine("Done!");
