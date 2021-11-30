/*
--- Day 1: Not Quite Lisp ---

Santa was hoping for a white Christmas, but his weather machine's "snow" function is powered by stars, and he's fresh out! To save Christmas, he needs you to collect fifty stars by December 25th.

Collect stars by helping Santa solve puzzles. Two puzzles will be made available on each day in the Advent calendar; the second puzzle is unlocked when you complete the first. Each puzzle grants one star. Good luck!

Here's an easy puzzle to warm you up.

Santa is trying to deliver presents in a large apartment building, but he can't find the right floor - the directions he got are a little confusing. He starts on the ground floor (floor 0) and then follows the instructions one character at a time.

An opening parenthesis, (, means he should go up one floor, and a closing parenthesis, ), means he should go down one floor.

The apartment building is very tall, and the basement is very deep; he will never find the top or bottom floors.

For example:

    (()) and ()() both result in floor 0.
    ((( and (()(()( both result in floor 3.
    ))((((( also results in floor 3.
    ()) and ))( both result in floor -1 (the first basement level).
    ))) and )())()) both result in floor -3.

To what floor do the instructions take Santa?

Your puzzle answer was 74.
--- Part Two ---

Now, given the same instructions, find the position of the first character that causes him to enter the basement (floor -1). The first character in the instructions has position 1, the second character has position 2, and so on.

For example:

    ) causes him to enter the basement at character position 1.
    ()()) causes him to enter the basement at character position 5.

What is the position of the character that causes Santa to first enter the basement?
*/

use std::convert::TryFrom;

fn count_parenthesis(input: &str) -> i32 {
    let count_of_opening_brackets = i32::try_from(input.matches("(").count()).unwrap();
    let count_of_closing_brackets = i32::try_from(input.matches(")").count()).unwrap();
    count_of_opening_brackets - count_of_closing_brackets
}

fn find_first_basement_position(input: &str, floor: i32) -> u32 {
    let mut current_floor = 0;

    for (index, floor_move) in input.chars().enumerate() {
        if floor_move == '(' {
            current_floor += 1;
        } else if floor_move == ')' {
            current_floor -= 1;
        }

        if current_floor == floor {
            return u32::try_from(index + 1).unwrap();
        }
    }

    return 0;
}

pub fn part1(input: &str) -> i32 {
    count_parenthesis(&input)
}

pub fn part2(input: &str) -> u32 {
    find_first_basement_position(&input, -1)
}

#[cfg(test)]
mod tests {
    use crate::day1::{count_parenthesis, find_first_basement_position};

    #[test]
    fn test_part1_floor_0_1() {
        assert_eq!(count_parenthesis("(())"), 0);
    }

    #[test]
    fn test_part1_floor_0_2() {
        assert_eq!(count_parenthesis("()()"), 0);
    }

    #[test]
    fn test_part1_floor_3_1() {
        assert_eq!(count_parenthesis("((("), 3);
    }

    #[test]
    fn test_part1_floor_3_2() {
        assert_eq!(count_parenthesis("(()(()("), 3);
    }

    #[test]
    fn test_part1_floor_3_3() {
        assert_eq!(count_parenthesis("))((((("), 3);
    }

    #[test]
    fn test_part1_floor_minus_1_1() {
        assert_eq!(count_parenthesis("())"), -1);
    }

    #[test]
    fn test_part1_floor_minus_1_2() {
        assert_eq!(count_parenthesis("))("), -1);
    }

    #[test]
    fn test_part1_floor_minus_3_1() {
        assert_eq!(count_parenthesis(")))"), -3);
    }

    #[test]
    fn test_part1_floor_minus_3_2() {
        assert_eq!(count_parenthesis(")())())"), -3);
    }

    #[test]
    fn test_part2_1() {
        assert_eq!(find_first_basement_position(")", -1), 1);
    }

    #[test]
    fn test_part2_2() {
        assert_eq!(find_first_basement_position("()())", -1), 5);
    }
}
