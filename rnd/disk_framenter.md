## Decoding to parts

- Each index % 1 == file block size
- Each index % 2 == free space size

f = file block
. = free space
[0-9] = ID

```
1 2 3 4 5
^ ^ ^ ^ ^
f . f . f
0 - 1 - 2
```

## Unpacking

- Add the ID of the file for each block's size
- Add a . for the each free space's size

```
0..111....22222
```

## Reordering

- Mov one entry at a time
- From the end of the disk
- To the leftmost free space block 
- until there are no gaps remaining between file blocks
- this should leave all the free space at the end of the file

```
0..111....22222
02.111....2222.
022111....222..
0221112...22...
02211122..2....
022111222......
```

## Checksum

- Add up the result of:
- Multiplying each of these blocks' position with the file ID number it contains
- The leftmost block is in position 0
- If a block contains free space, skip it instead.

```
0 * 0 = 0
1 * 0 = 0
2 * 9 = 18
3 * 9 = 27
4 * 8 = 32
...
checksum = 1928
```
