using ProcessMemory;
using ProcessMemory.Types;
using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Linq;
using System.Reflection;
using YamlDotNet.Core;
using YamlDotNet.Core.Events;
using YamlDotNet.Serialization;
using YamlDotNet.Serialization.NamingConventions;

namespace MemCore
{
    public class MemPointer
    {
        public string Name { get; set; }
        public int BaseOffset { get; set; }
        public int[] LevelOffsets { get; set; } = new int[0];
        public int ValueOffset { get; set; }
        public Type Type { get; set; } = typeof(long);
        public object? Default { get; set; }

        private Process? Process { get; set; }
        private ProcessMemoryHandler? MemoryHandler { get; set; }
        private MultilevelPointer? Pointer { get; set; }

        public MemPointer (string name, int baseOffset, List<int> levelOffsets, int valueOffset, Type type, object? defaultValue=null)
        {
            Name = name;
            BaseOffset = baseOffset;
            LevelOffsets = levelOffsets.ToArray();
            ValueOffset = valueOffset;
            Type = type;
            Default = defaultValue;
        }

        public MemPointer (string name, int baseOffset, int[] levelOffsets, int valueOffset, Type type, object? defaultValue=null)
        {
            Name = name;
            BaseOffset = baseOffset;
            LevelOffsets = levelOffsets;
            ValueOffset = valueOffset;
            Type = type;
            Default = defaultValue;
        }

        public unsafe void AttachProcess(Process process)
        {
            Process = process;
            MemoryHandler = new ProcessMemoryHandler(Process.Id);

            var baseAddress = NativeWrappers.GetProcessBaseAddress(Process.Id, PInvoke.ListModules.LIST_MODULES_64BIT);

            var levelOffsets = LevelOffsets.Select(x => (long)x).ToArray();

            Pointer = new MultilevelPointer(MemoryHandler, IntPtr.Add(baseAddress, BaseOffset), levelOffsets);
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
            if (Type == typeof(int))
                return Pointer.DerefInt(ValueOffset);
            if (Type == typeof(long))
                return Pointer.DerefLong(ValueOffset);
            if (Type == typeof(float))
                return Pointer.DerefFloat(ValueOffset);
            if (Type == typeof(double))
                return Pointer.DerefDouble(ValueOffset);
            if (Type == typeof(string))
                return Pointer.DerefUnicodeString(ValueOffset, 100);
            throw new ArgumentException($"Invalid type '{Type.Name}'");
        }

    }
}
