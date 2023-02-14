using YamlDotNet.Serialization;

namespace MemCore
{

    public class GameVersion
    {
        public string Name { get; set; }
        public string Description { get; set; }
        public byte[] Hash { get; set; }
        public Dictionary<string, int> Addresses { get; set; }

        public GameVersion (string name, string description, byte[] hash, Dictionary<string, int> addresses)
        {
            Name = name;
            Description = description;
            Hash = hash;
            Addresses = addresses;
        }
    }


    public class MemStruct
    {
        public string Name { get; set; }
        public int Pack { get; set; }
        public int Size { get; set; }
        public Dictionary<string, Field> Fields { get; set; }

        public MemStruct (string name, int pack, int size, Dictionary<string, Field> fields)
        {
            Name = name;
            Pack = pack;
            Size = size;
            Fields = fields;
        }
    }

    public class Field
    {
        public string Name { get; set; }
        public int Offset { get; set; }
        public Type Type { get; set; }
        public object? Default { get; set; }

        public Field (string name, int offset, Type type, object? defaultValue=null)
        {
            Name = name;
            Offset = offset;
            Type = type;
            Default = defaultValue;
        }
    }

    public class State
    {
        public string Name { get; set; }
        public int[] Levels { get; set; }
        public int Offset { get; set; }
        public string Type { get; set; }
        public object? Default { get; set; }

        public State (string name, int[] levels, int offset, string type, object? defaultValue=null)
        {
            Name = name;
            Levels = levels;
            Offset = offset;
            Type = type;
            Default = defaultValue;
        }
    }


    public class MemConfig
    {

        public Dictionary<string, MemPointer>? Pointers { get; set; }

        public string? ConfString { get; set; }
        public string? GameVersion { get; set; }

        private Dictionary<string, object>? Config { get; set; }

        public Dictionary<string, GameVersion> GameVersions
        {
            get
            {
                if (Config == null)
                    throw new Exception("Config not parsed yet");
                if (Config.ContainsKey("GameVersions"))
                    return (Dictionary<string, GameVersion>)Config["GameVersions"];
                else
                    return new Dictionary<string, GameVersion>();
            }
        }

        public Dictionary<string, State> States
        {
            get
            {
                if (Config == null)
                    throw new Exception("Config not parsed yet");
                if (Config.ContainsKey("States"))
                    return (Dictionary<string, State>)Config["States"];
                else
                    return new Dictionary<string, State>();
            }
        }

        public Dictionary<string, MemStruct> Structs
        {
            get
            {
                if (Config == null)
                    throw new Exception("Config not parsed yet");
                if (Config.ContainsKey("Structs"))
                    return (Dictionary<string, MemStruct>)Config["Structs"];
                else
                    return new Dictionary<string, MemStruct>();
            }
        }


        public void Parse(string? yamlFile)
        {
            if (yamlFile != null)
                ConfString = File.ReadAllText(yamlFile);
            else if (ConfString == null)
                throw new Exception("No config string or file provided");

            var config = new Dictionary<string, object>();

            var deserializer = new DeserializerBuilder().Build();
            var raw_config = (Dictionary<object, object>?) deserializer.Deserialize(new StringReader(ConfString));

            if (raw_config == null)
                return;

            // Iterate over the deserialized object and dispatch to the appropriate parsers
            foreach (var conf in raw_config)
            {
                if (conf.Key.ToString().ToUpper() == "GAME_VERSIONS")
                    config.Add("GameVersions", _ParseGameVersions(ToObjDict(conf.Value)));
                else if (conf.Key.ToString().ToUpper() == "STATES")
                    config.Add("States", _ParseStates(ToObjDict(conf.Value)));
                else if (conf.Key.ToString().ToUpper() == "STRUCTS")
                    config.Add("Structs", _ParseStructs(ToObjDict(conf.Value)));
                else
                    config.Add(conf.Key.ToString(), conf.Value);
            }

            // Set the config
            Config = config;
        }


        public void Build(string? gameVersion)
        {
            // Handle nulls
            if (Config == null)
                throw new Exception("Config not parsed yet");
            if (gameVersion != null)
                GameVersion = gameVersion;
            else if (GameVersion == null)
                throw new Exception("No game version provided");

            // Get the game version
            var thisVersion = GameVersions[GameVersion];

            // Process Config into MemPointer instances
            var pointers = new Dictionary<string, MemPointer>();

            // Iterate over States to build pointers
            foreach (var state in States)
            {
                var type = state.Value.Type;

                // Determine if the type is a data type or a struct
                if (Structs.ContainsKey(type))
                {
                    var _pointers = _BuildStructPointers(Structs[type], state.Value, thisVersion);
                    foreach (var p in _pointers)
                        pointers.Add(p.Name, p);
                }
                else
                {
                    pointers.Add(state.Key, _BuildStatePointer(state.Value, thisVersion));
                }
            }

            Pointers = pointers;
        }


        private static Dictionary<string, GameVersion> _ParseGameVersions(Dictionary<object, object> versions)
        {
            var gameVersions = new Dictionary<string, GameVersion>();
            foreach (var item in versions)
            {
                var name = (string)item.Key;
                var val = ToObjDict(item.Value);
                var desc = (string)val["Description"];
                var hash = ToObjList(val["Hash"]).Select(b => Convert.ToByte((string)b, 16)).ToArray(); // There must be a better way...
                var pointers = ToObjDict(val["Pointers"]);
                var addressesDict = new Dictionary<string, int>();
                foreach (var addr in pointers)
                {
                    var aKey = (string)addr.Key;
                    var aVal = Convert.ToInt32((string)addr.Value, 16);
                    addressesDict.Add(aKey, aVal);
                }
                gameVersions.Add(name, new GameVersion(name, desc, hash, addressesDict));
            }
            return gameVersions;
        } 

        private static Dictionary<string, MemStruct> _ParseStructs(Dictionary<object, object> structs)
        {
            var memStructs = new Dictionary<string, MemStruct>();
            foreach (var item in structs)
            {
                var structName = (string)item.Key;
                var structVal = ToObjDict(item.Value);
                var pack = Convert.ToInt32((string)structVal["Pack"]);
                var size = Convert.ToInt32((string)structVal["Size"], 16);
                var fields = ToObjDict(structVal["Fields"]);
                var fieldsDict = new Dictionary<string, Field>();
                foreach (var field in fields)
                {
                    var fieldName = (string)field.Key;
                    var fieldVal = ToObjDict(field.Value);
                    var fieldObj = new Field(
                        fieldName, 
                        Convert.ToInt32((string)fieldVal["Offset"], 16),
                        Type.GetType(TypeDictionary[(string)fieldVal["Type"]]),
                        fieldVal.ContainsKey("Default") ? fieldVal["Default"] : null
                    );
                    fieldsDict.Add(fieldName, fieldObj);
                }
                memStructs.Add(structName, new MemStruct(structName, pack, size, fieldsDict));
            }
            return memStructs;
        }

        private static Dictionary<string, State> _ParseStates(Dictionary<object, object> states)
        {
            var States = new Dictionary<string, State>();
            foreach (var item in states)
            {
                var name = (string)item.Key;
                var val = (Dictionary<object, object>)item.Value;
                // TODO: Allow null levels
                var levels = ToObjList(val["Levels"]).Select(b => Convert.ToInt32((string)b, 16)).ToArray();
                var offset = Convert.ToInt32((string)val["Offset"], 16);
                var type = (string)val["Type"];
                States.Add(name, new State(name, levels, offset, type, val.ContainsKey("Default") ? val["Default"] : null));
            }
            return States;
        }

        private static MemPointer _BuildStatePointer(State state, GameVersion gameVersion)
        {
            var baseOffset = gameVersion.Addresses[state.Name];
            var memPointer = new MemPointer(
                state.Name, 
                baseOffset, 
                state.Levels, 
                state.Offset, 
                Type.GetType(TypeDictionary[state.Type]), 
                state.Default
            );
            return memPointer;
        }

        private static List<MemPointer> _BuildStructPointers(MemStruct memStruct, State state, GameVersion gameVersion)
        {
            var pointers = new List<MemPointer>();

            // State details for the whole Struct
            var baseOffset = gameVersion.Addresses[state.Name];
            var levels = state.Levels;
            var valueOffset = state.Offset;

            // Struct details
            // var structPack = memStruct.Pack;
            // var structSize = memStruct.Size;

            // Build pointer for each struct field
            foreach (var field in memStruct.Fields)
                pointers.Add(
                    new MemPointer(
                        field.Key, 
                        baseOffset, 
                        levels,
                        valueOffset + field.Value.Offset, 
                        field.Value.Type,
                        field.Value.Default
                    )
                );

            return pointers;
        }

        private static Dictionary<object, object> ToObjDict(object obj) => (Dictionary<object, object>)obj;
        private static List<object> ToObjList(object obj) => (List<object>)obj;

        private static Dictionary<string, string> TypeDictionary = new Dictionary<string, string>
        {
            { "int", "System.Int32" },
            { "long", "System.Int64" },
            { "float", "System.Single" },
            { "double", "System.Double" },
            { "decimal", "System.Decimal" }
        };
    }

}
