/*
--- Day 3: Perfectly Spherical Houses in a Vacuum ---

Santa is delivering presents to an infinite two-dimensional grid of houses.

He begins by delivering a present to the house at his starting location, and then an elf at the North Pole calls him via radio and tells him where to move next. Moves are always exactly one house to the north (^), south (v), east (>), or west (<). After each move, he delivers another present to the house at his new location.

However, the elf back at the north pole has had a little too much eggnog, and so his directions are a little off, and Santa ends up visiting some houses more than once. How many houses receive at least one present?

For example:

    > delivers presents to 2 houses: one at the starting location, and one to the east.
    ^>v< delivers presents to 4 houses in a square, including twice to the house at his starting/ending location.
    ^v^v^v^v^v delivers a bunch of presents to some very lucky children at only 2 houses.

--- Part Two ---

The next year, to speed up the process, Santa creates a robot version of himself, Robo-Santa, to deliver presents with him.

Santa and Robo-Santa start at the same location (delivering two presents to the same starting house), then take turns moving based on instructions from the elf, who is eggnoggedly reading from the same script as the previous year.

This year, how many houses receive at least one present?

For example:

    ^v delivers presents to 3 houses, because Santa goes north, and then Robo-Santa goes south.
    ^>v< now delivers presents to 3 houses, and Santa and Robo-Santa end up back where they started.
    ^v^v^v^v^v now delivers presents to 11 houses, with Santa going one direction and Robo-Santa going the other.
*/

use std::collections::HashMap;

pub fn part1(input: &str) -> i32 {
    let mut coordinates = HashMap::new();
    let mut current_x: i32 = 0;
    let mut current_y: i32 = 0;

    coordinates.insert((current_x, current_y), 0);

    for c in input.chars() {
        match c {
            '>' => current_x += 1,
            '<' => current_x -= 1,
            '^' => current_y += 1,
            'v' => current_y -= 1,
            _ => {}
        }

        coordinates.insert((current_x, current_y), 0);
    }

    coordinates.into_iter().count() as i32
}

pub fn part2(input: &str) -> i32 {
    let mut coordinates = HashMap::new();
    let mut santa_current_x: i32 = 0;
    let mut santa_current_y: i32 = 0;
    let mut robosanta_current_x: i32 = 0;
    let mut robosanta_current_y: i32 = 0;

    coordinates.insert((santa_current_x, santa_current_y), 0);
    coordinates.insert((robosanta_current_x, robosanta_current_y), 0);

    for (i, c) in input.chars().enumerate() {
        let mut current_x = &mut santa_current_x;
        let mut current_y = &mut santa_current_y;

        match i % 2 {
            0 => {
                current_x = &mut santa_current_x;
                current_y = &mut santa_current_y;
            }
            1 => {
                current_x = &mut robosanta_current_x;
                current_y = &mut robosanta_current_y;
            }
            _ => {}
        }

        match c {
            '>' => *current_x += 1,
            '<' => *current_x -= 1,
            '^' => *current_y += 1,
            'v' => *current_y -= 1,
            _ => {}
        }

        coordinates.insert((santa_current_x, santa_current_y), 0);
        coordinates.insert((robosanta_current_x, robosanta_current_y), 0);
    }

    coordinates.into_iter().count() as i32
}

#[cfg(test)]
mod tests {
    use crate::day3::{part1, part2};

    #[test]
    fn test_part1_1() {
        assert_eq!(part1(">"), 2)
    }

    #[test]
    fn test_part1_2() {
        assert_eq!(part1("^>v<"), 4)
    }

    #[test]
    fn test_part1_3() {
        assert_eq!(part1("^v^v^v^v^v"), 2)
    }

    #[test]
    fn test_part2_1() {
        assert_eq!(part2("^v"), 3)
    }

    #[test]
    fn test_part2_2() {
        assert_eq!(part2("^>v<"), 3)
    }

    #[test]
    fn test_part2_3() {
        assert_eq!(part2("^v^v^v^v^v"), 11)
    }
}
