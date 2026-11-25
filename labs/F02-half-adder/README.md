# F02 · 半加器：第一个真实电路

对应 F2（Logisim 安装和使用）+ F3（数字逻辑电路基础，见 [docs/01](../../docs/01-数字逻辑电路基础.md) 第 2 节）。

**目标**：用真实的门电路做出 `S = A XOR B`、`C = A AND B`，也就是讲义里那张真值表的物理实现。

---

## 先说结论：这个电路已经验证过了

生成 `.circ` 之后，我用你本机的 **Logisim Evolution 4.0.0 命令行无头模式**真实跑了一遍：

```
$ logisim-evolution.exe -t stats half_adder.circ
4   4   Pin       Wiring
1   1   AND Gate  Gates
1   1   XOR Gate  Gates
6   6   TOTAL

$ logisim-evolution.exe -w main vectors.txt half_adder.circ
Loading test vector "vectors.txt"...
Running 4 vectors...
1 2 3 4
Passed: 4, Failed: 0
```

所以你打开它时，应该直接能看到正确结果。如果结果不对，先怀疑自己点错了引脚，而不是电路。

## 文件

| 文件 | 用途 |
|---|---|
| `half_adder.circ` | 电路文件（Logisim Evolution 4.x 格式） |
| `vectors.txt` | 测试向量：4 组输入和期望输出 |
| `run_test.bat` | Windows 一键复验（双击即可） |

## 方式一：在 GUI 里打开（推荐，先看这个）

1. 打开 Logisim Evolution
2. `File → Open` → 选 `half_adder.circ`
3. 用 **Poke Tool**（手形图标）点击输入引脚 `A` / `B`，每点一次在 0/1 之间切换
4. 观察输出引脚 `S`（和）与 `C`（进位）

依次拨出 00 / 01 / 10 / 11，把看到的 S、C 记下来，和 `vectors.txt` 对照。

## 方式二：命令行复验

在本目录执行（或双击 `run_test.bat`）：

```bash
"D:\Program Files\logisim-evolution\logisim-evolution.exe" -o en --no-splash -w main vectors.txt half_adder.circ
```

参数含义：
- `-o en`：界面语言设英文，避免终端中文乱码
- `--no-splash`：不显示启动画面
- `-w main vectors.txt half_adder.circ`：在 `main` 电路上跑 `vectors.txt`，项目文件是 `half_adder.circ`
- `-t stats`：无 GUI 加载电路并打印元件统计，用来快速检查文件能不能被读

## 电路结构

| 元件 | 坐标 | 作用 |
|---|---|---|
| Pin A | (100,100) | 输入 A |
| Pin B | (100,300) | 输入 B |
| XOR Gate | (300,140) | 输出 `S = A ⊕ B` |
| AND Gate | (300,240) | 输出 `C = A · B` |
| Pin S | (400,140) | 输出（和），朝西 |
| Pin C | (400,240) | 输出（进位），朝西 |

**坐标为什么这么算**：Logisim 里 Gate 的 `loc` 是**输出引脚**的位置；设 `size=30` 时，两个输入引脚在 `(x-30, y-10)` 和 `(x-30, y+10)`。所以 XOR 的输入点是 (270,130) 与 (270,150)，导线要连到这两个点才算接上。Pin 的 `loc` 就是它自己的引脚点，可以直接连。

## 测试向量怎么读

```
A B S C      <- 第一行：信号名，对应电路里 Pin 的 label
0 0 0 0      <- 后面每行：一组取值
0 1 1 0
1 0 1 0
1 1 0 1
```

Logisim 自动把**输入 Pin**（A、B）当作施加的激励，把**输出 Pin**（S、C）当作期望值，逐行比对。第一行不需要斜杠分隔，也不用标注方向。

## 一个真实的坑：交叉线不相连

A 的横线 `(200,230) → (270,230)` 和 B 的竖线 `(230,150) → (230,250)` 在 **(230,230)** 处交叉。

在 Logisim 里，**交叉的导线默认不连接**——只有端点正好落在另一条线上、或者你显式加了连接点（junction）才会连通。测试向量能 4/4 通过，恰恰证明 A 和 B 没有被短接。

如果你在那个交叉点加了连接点，A 和 B 会被短接，仿真就会出错。这是练习 3 要故意做的事。

> 真实电路图里也有同样约定：交叉不连、有黑点才连。 Logisim 只是照搬了这个习惯。

## 练习

1. **手动复验**：GUI 里依次拨 A/B = 00 / 01 / 10 / 11，把 S、C 记下来，和 `vectors.txt` 对照。
2. **学会读失败信息**：把 `vectors.txt` 最后一行 `1 1 0 1` 故意改成 `1 1 0 0`，重跑 `run_test.bat`，观察输出里的 `Failed: 1` 和它指出的那一行。改回来。
3. **制造短接**：在 GUI 里给 (230,230) 交叉点加一个连接点，看仿真变成什么样，然后撤销。
4. **升级成全加器**：加第三个输入 `Cin`，用两个半加器 + 一个 OR 门，写出 8 行新的测试向量。（提示：`S = A ⊕ B ⊕ Cin`，`Cout = (A·B) + (Cin·(A⊕B))`）
5. **消除交叉**：用 Logisim 的 **Tunnel** 元件（同名标签自动相连，不用画线）重画这个电路，让图面完全干净。

## 下一步

→ 用同样的方法做 F4 的**状态机**：加一个寄存器和一个时钟，观察"有记忆的电路"和这里的组合逻辑有什么不同。
