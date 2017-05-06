# Human Ressource Machine - Language Specification

---

General
-------

- Turysembler is case sensitive
- Whitespace before any command will be ignored
- Trailig whitespace will be ignored
- There a no literals of any kind.
  Therefore, a number ALWAYS represents the index
  of a floor tile / memory cell.
  It is always possible to surround a number by
 square brackets to use it as a pointer variable.

Comments
--------

- Comments start with an '#'
- It's recommended to not write a comment
  to the same line as an instruction.
  It might work some times, but it will
  certainly crash at some other times.
- Comments will be compiled, too. They
  will be transformed into HRM-Comments


Single instructions
-------------------

- `push <num>` - saves ACC to field <num>
- `pull <num>` - sets ACC to value of field <num>
- `incr <num>` - increments value of field <num> by 1
- `decr <num>` - decrements value of field <num> by 1

- `<num> = <arithmetic operations>`
    - saves the result of the arithmetic operation to
      field <num>


Arithmetic operations
---------------------
- `<num1> + <num2>`
    - addition of values
- `<num1> * <num2> | <num3>`
    - multiplications of
      fields <num1> and
      <num2>. The third
      field <num3> will be
      used as an temporary
      storage. So make shure
      to choose a field no
      loger needed, hence it
      will be overwritten.


Loops
-----

- Start each loop with a `loop` instruction
- Loops can be closed by a `repeat`-instruction
  or by an `endif` instruction followed by
  a condition.
- "repeat-loops" will never be stoped -> endless
- "endif-loops" will be stoped once the condition
  is TRUE


Conditions
----------

- implemented conditions are:
  - `<num1> = <num2>`
  - `<num1> < <num2>`
  - `<num1> > <num2>`
- return TRUE if the expression
  is true


Conditional branching
---------------------

Syntax:

    if <condition>
        <instructions...>
    else
        <instructions...>
    fi

The else block is needed, but may be empty.

