def шипение_жужжание(номер):
    if not номер % 15:
        return "ШипениеЖужжание"
    if not номер % 3:
        return "Шипение"
    if not номер % 5:
        return "Жужжание"
    return str(номер)


for номер in range(100):
    print(шипение_жужжание(номер))
