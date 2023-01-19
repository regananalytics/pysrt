using ProcessMemory;
using ProcessMemory.Types;
using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Linq;
using YamlDotNet.Core;
using YamlDotNet.Core.Events;
using YamlDotNet.Serialization;
using YamlDotNet.Serialization.NamingConventions;

namespace MemCore
{
    public class MemPointer
    {
        public Process? Process { get; set; }
        public ProcessMemoryHandler? MemoryHandler { get; set; }
        public MultilevelPointer? Pointer { get; set; }
        public long BaseOffset { get; set; }
        public List<long> LevelOffsets { get; set; } = new List<long>();
        public int ValueOffset { get; set; }
        public Type Type { get; set; } = typeof(long);
        public object? Default { get; set; }
        public Dictionary<string, MemPointer> Children { get; set; } = new Dictionary<string, MemPointer>();

        public void InheritProperties(MemPointer parent)
        {
            if (BaseOffset == 0) BaseOffset = parent.BaseOffset;
            if (!LevelOffsets.Any()) LevelOffsets = parent.LevelOffsets;
            if (Type == null) Type = parent.Type;
        }

        public void AttachProcess(Process process)
        {
            Process = process;
            MemoryHandler = new ProcessMemoryHandler(Process.Id);
            var baseAddress = new IntPtr(BaseOffset);
            var levelOffsets = LevelOffsets.Select(x => (long)x).ToArray();
            Pointer = new MultilevelPointer(MemoryHandler, baseAddress, levelOffsets);
            Update();
        }

        public void Update()
        {
            Pointer?.UpdatePointers();
        }

        public object? Deref()
        {
            Update();
            if (Pointer == null || Pointer.IsNullPointer)
                return Default;
            var offset = ValueOffset;
            if (Type == typeof(int))
                return Pointer.DerefInt(offset);
            if (Type == typeof(long))
                return Pointer.DerefLong(offset);
            if (Type == typeof(float))
                return Pointer.DerefFloat(offset);
            if (Type == typeof(double))
                return Pointer.DerefDouble(offset);
            if (Type == typeof(string))
                return Pointer.DerefUnicodeString(offset, 100);
            throw new ArgumentException($"Invalid type '{Type.Name}'");
        }

    }

    public static class MemPointerParser
    {
        private static readonly Deserializer deserializer = (Deserializer) new DeserializerBuilder()
            .WithNamingConvention(PascalCaseNamingConvention.Instance)
            .WithTypeConverter(new TypeConverter())
            .Build();

        public static Dictionary<string, MemPointer> Parse(string yaml)
        {
            var pointers = deserializer.Deserialize<Dictionary<string, MemPointer>>(yaml);

            // Inherit properties from parent pointers
            foreach (var kv in pointers)
            {
                var pointer = kv.Value;
                if (pointer.Children.Any())
                {
                    foreach (var child in pointer.Children.Values)
                    {
                        child.InheritProperties(pointer);
                    }
                }
            }

            return pointers;
        }

        private class TypeConverter : IYamlTypeConverter
        {
            private static Dictionary<string, Type> _stringToType = new Dictionary<string, Type>
            {
                {"Int", typeof(int)},
                {"Long", typeof(long)},
                {"Float", typeof(float)},
                {"Double", typeof(double)},
                {"String", typeof(string)},
                {"Byte", typeof(byte)},
                {"SByte", typeof(sbyte)},
                {"Short", typeof(short)},
                {"UShort", typeof(ushort)},
                {"Int24", typeof(Int24)},
                {"UInt24", typeof(UInt24)},
                {"UInt", typeof(uint)},
                {"ULong", typeof(ulong)},
                {"SpanByte", typeof(Span<byte>)},
                {"ByteArray", typeof(byte[])},
                {"ASCIIString", typeof(string)},
                {"UnicodeString", typeof(string)},
            };

            public bool Accepts(Type type) => type == typeof(Type);

            public object ReadYaml(IParser parser, Type expectedType)
            {
                var scalar = (Scalar)parser.Current;
                if (_stringToType.TryGetValue(scalar.Value, out var type))
                {
                    parser.MoveNext();
                    return type;
                }
                else
                {
                    throw new ArgumentException($"Invalid Type '{scalar.Value}'");
                }
            }

            public void WriteYaml(IEmitter emitter, object value, Type type)
            {
                var typeName = value.ToString();
                emitter.Emit(new Scalar(typeName));
            }
        }
    }
}
