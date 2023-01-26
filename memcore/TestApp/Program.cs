// See https://aka.ms/new-console-template for more information
using MemCore;
using ProcessMemory;
using System.Diagnostics;
using System.Reflection;
using YamlDotNet.RepresentationModel;
using System.Buffers;

string gameName = "re2";
string gameConf = @"C:/Users/verti/Documents/GitHub/pysrt/memconf/" + gameName + ".yaml";


// Load the process
var process = Process.GetProcessesByName(gameName)?.FirstOrDefault();

// Parse the config
var memConf = new MemConfig();
memConf.Parse(gameConf);
memConf.Build("RE2_WW_20220613_1");



Console.WriteLine("Done!");
