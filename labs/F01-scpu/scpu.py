#!/usr/bin/env python3
"""F01 - 一个只有 4 条指令的最小 CPU 模拟器。

对齐「一生一芯」F 阶段 sCPU 的指令集思路: add / li / bner0 / out。
目标程序: 计算 1 + 2 + ... + 10 = 55。

运行:
    python scpu.py            # 打印每一步的状态转移
    python scpu.py --quiet    # 只输出最终结果

零依赖，只用 Python 标准库。
"""

import sys

# 程序就是数据: 一段指令列表，存在「指令存储器」里。
# PC (程序计数器) 指向当前要执行的那一条。
SOURCE = """
    LI    r1, 0        # r1 = sum, 初始 0
    LI    r2, 10       # r2 = i, 从 10 开始往下数
    LI    r3, -1       # r3 = 步长 -1
    ADD   r1, r1, r2   # sum = sum + i
    ADD   r2, r2, r3   # i = i - 1
    BNER0 r2, 3        # 若 i != r0(=0), 跳回第 3 条继续循环
    OUT   r1           # 把 sum 输出
"""

ISA = {
    "LI":    "LI rd, imm        -> rd = imm",
    "ADD":   "ADD rd, rs1, rs2  -> rd = rs1 + rs2",
    "BNER0": "BNER0 rs, target  -> if rs != 0 then PC = target",
    "OUT":   "OUT rs            -> 输出 rs 的值",
}


def parse(source):
    """把汇编文本解析成 [(op, [args...]), ...]。"""
    program = []
    for raw in source.strip().splitlines():
        line = raw.split("#")[0].strip().replace(",", " ")
        if not line:
            continue
        parts = line.split()
        program.append((parts[0].upper(), parts[1:]))
    return program


class CPU:
    """一台极简 CPU: 4 个寄存器 + PC + 一段程序，就是一个状态机。"""

    REGS = 4

    def __init__(self, program):
        self.program = program
        self.reg = [0] * self.REGS
        self.pc = 0
        self.steps = 0
        self.outputs = []
        self.halted = False

    @staticmethod
    def _index(token):
        return int(token.lower().lstrip("r"))

    def _read(self, token):
        """读操作数: r1 是寄存器, 10 / -1 是立即数。"""
        if token.lower().startswith("r"):
            return self.reg[self._index(token)]
        return int(token, 0)

    def step(self):
        """执行一条指令 —— 这就是 CPU 的一个时钟周期。"""
        if self.pc >= len(self.program):
            self.halted = True
            return None

        pc_now = self.pc
        op, args = self.program[self.pc]

        if op == "LI":
            self.reg[self._index(args[0])] = self._read(args[1])
            self.pc += 1
        elif op == "ADD":
            rd, rs1, rs2 = args
            self.reg[self._index(rd)] = self._read(rs1) + self._read(rs2)
            self.pc += 1
        elif op == "BNER0":
            # BNER0 = Branch if Not Equal to R0，r0 恒为 0
            self.pc = self._read(args[1]) if self._read(args[0]) != 0 else self.pc + 1
        elif op == "OUT":
            self.outputs.append(self._read(args[0]))
            self.pc += 1
        else:
            raise ValueError(f"未知指令: {op} @ pc={pc_now}")

        self.reg[0] = 0  # r0 恒为 0，任何写入都无效（RISC-V x0 同理）
        self.steps += 1
        return pc_now, op, args

    def snapshot(self):
        return " ".join(f"r{i}={v:<4}" for i, v in enumerate(self.reg))


def main():
    quiet = "--quiet" in sys.argv
    cpu = CPU(parse(SOURCE))

    if not quiet:
        print("=" * 66)
        print(" F01 · 最小 CPU 模拟器  (LI / ADD / BNER0 / OUT)")
        print(" 程序: 1 + 2 + ... + 10")
        print("=" * 66)
        print("指令集:")
        for text in ISA.values():
            print(f"  {text}")
        print("-" * 66)
        print(f"{'step':<6}{'pc':<6}{'instruction':<24}registers after")
        print("-" * 66)

    while not cpu.halted and cpu.steps < 1000:
        result = cpu.step()
        if result is None:
            break
        pc_now, op, args = result
        if not quiet:
            instr = f"{op} {' '.join(args)}"
            print(f"{cpu.steps:<6}{pc_now:<6}{instr:<24}{cpu.snapshot()}")

    if cpu.steps >= 1000:
        print("检测到可能的死循环，已停止（检查 BNER0 的跳转目标）")
        return 1

    if not quiet:
        print("-" * 66)
    result = cpu.outputs[-1] if cpu.outputs else None
    print(f"共执行 {cpu.steps} 条指令，OUT 输出 = {cpu.outputs}")
    print(f"1 + 2 + ... + 10 = {result}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
