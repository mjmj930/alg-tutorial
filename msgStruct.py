from construct import Struct, Int16ub, Int32ub, Array, Default, this

# 结构体一
Struct1 = Struct(
    "field1" / Default(Int16ub, 0xFFFF),  # 默认值 0xFFFF
    "field2" / Default(Int32ub, 0xFFFFFFFF)  # 默认值 0xFFFFFFFF
)

# 结构体二
Struct2 = Struct(
    "param1" / Default(Int16ub, 0x0001),  # 默认值 0x0001
    "param2" / Default(Int32ub, 0xDEADBEEF),  # 默认值 0xDEADBEEF
    "array_size" / Default(Int16ub, 5),  # 默认数组大小 5
    "struct1_array" / Array(
        this.array_size,  # 显式引用已赋值的 array_size
        Struct1
    )
)

# 直接使用默认值
default_array_size = 5  # 默认的 array_size 值是 5

# 为 struct1_array 提供默认值
default_struct1_array = [{} for _ in range(default_array_size)]

# 构建 Struct2 实例
packed_data = Struct2.build({
    "struct1_array": default_struct1_array
})

# 输出
print("Packed Data (HEX):", packed_data)
