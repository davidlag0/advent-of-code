/*
--- Day 2: I Was Told There Would Be No Math ---

The elves are running low on wrapping paper, and so they need to submit an order for more. They have a list of the dimensions (length l, width w, and height h) of each present, and only want to order exactly as much as they need.

Fortunately, every present is a box (a perfect right rectangular prism), which makes calculating the required wrapping paper for each gift a little easier: find the surface area of the box, which is 2*l*w + 2*w*h + 2*h*l. The elves also need a little extra paper for each present: the area of the smallest side.

For example:

    A present with dimensions 2x3x4 requires 2*6 + 2*12 + 2*8 = 52 square feet of wrapping paper plus 6 square feet of slack, for a total of 58 square feet.
    A present with dimensions 1x1x10 requires 2*1 + 2*10 + 2*10 = 42 square feet of wrapping paper plus 1 square foot of slack, for a total of 43 square feet.

All numbers in the elves' list are in feet. How many total square feet of wrapping paper should they order?

--- Part Two ---

The elves are also running low on ribbon. Ribbon is all the same width, so they only have to worry about the length they need to order, which they would again like to be exact.

The ribbon required to wrap a present is the shortest distance around its sides, or the smallest perimeter of any one face. Each present also requires a bow made out of ribbon as well; the feet of ribbon required for the perfect bow is equal to the cubic feet of volume of the present. Don't ask how they tie the bow, though; they'll never tell.

For example:

    A present with dimensions 2x3x4 requires 2+2+3+3 = 10 feet of ribbon to wrap the present plus 2*3*4 = 24 feet of ribbon for the bow, for a total of 34 feet.
    A present with dimensions 1x1x10 requires 1+1+1+1 = 4 feet of ribbon to wrap the present plus 1*1*10 = 10 feet of ribbon for the bow, for a total of 14 feet.

How many total feet of ribbon should they order?
*/

pub struct Present {
    pub length: u32,
    pub width: u32,
    pub height: u32,
    pub surface: u32,
    pub extra: u32,
    pub total: u32,
    pub ribbon_for_present: u32, // part 2
    pub ribbon_for_bow: u32,     // part 2
    pub total_ribbon: u32,       // part 2
}

impl Present {
    pub fn new(dimensions_str: &str) -> Result<Present, &str> {
        let dimensions_list: Vec<&str> = dimensions_str.split('x').collect();

        let length = dimensions_list[0].parse::<u32>().unwrap();
        let width = dimensions_list[1].parse::<u32>().unwrap();
        let height = dimensions_list[2].parse::<u32>().unwrap();
        let surface = 2 * length * width + 2 * width * height + 2 * height * length;
        let extra = vec![length * width, width * height, height * length]
            .iter()
            .min()
            .unwrap()
            .clone();
        let total = surface + extra;

        // Part 2
        let ribbon_for_present = vec![
            2 * length + 2 * width,
            2 * width + 2 * height,
            2 * height + 2 * length,
        ]
        .iter()
        .min()
        .unwrap()
        .clone();
        let ribbon_for_bow = length * width * height;
        let total_ribbon = ribbon_for_present + ribbon_for_bow;

        Ok(Present {
            length,
            width,
            height,
            surface,
            extra,
            total,
            ribbon_for_present, // part 2
            ribbon_for_bow,     // part 2
            total_ribbon,       // part 2
        })
    }
}

pub fn part1(input: &str) -> u32 {
    let list_of_dimensions: Vec<&str> = input.lines().collect();
    let mut total_paper = 0;

    for dimensions in list_of_dimensions {
        total_paper += Present::new(&dimensions).unwrap().total;
    }

    total_paper
}

pub fn part2(input: &str) -> u32 {
    let list_of_dimensions: Vec<&str> = input.lines().collect();
    let mut total_ribbon = 0;

    for dimensions in list_of_dimensions {
        total_ribbon += Present::new(&dimensions).unwrap().total_ribbon;
    }

    total_ribbon
}

#[cfg(test)]
mod tests {
    use crate::day2::{part1, part2, Present};

    #[test]
    fn test_part1_1() {
        assert_eq!(Present::new("2x3x4").unwrap().length, 2);
        assert_eq!(Present::new("2x3x4").unwrap().width, 3);
        assert_eq!(Present::new("2x3x4").unwrap().height, 4);
        assert_eq!(Present::new("2x3x4").unwrap().surface, 52);
        assert_eq!(Present::new("2x3x4").unwrap().extra, 6);
        assert_eq!(Present::new("2x3x4").unwrap().total, 58);
        assert_eq!(Present::new("2x3x4").unwrap().ribbon_for_present, 10); // part 2
        assert_eq!(Present::new("2x3x4").unwrap().ribbon_for_bow, 24); // part 2
        assert_eq!(Present::new("2x3x4").unwrap().total_ribbon, 34); // part 2
    }

    #[test]
    fn test_part1_2() {
        assert_eq!(Present::new("1x1x10").unwrap().length, 1);
        assert_eq!(Present::new("1x1x10").unwrap().width, 1);
        assert_eq!(Present::new("1x1x10").unwrap().height, 10);
        assert_eq!(Present::new("1x1x10").unwrap().surface, 42);
        assert_eq!(Present::new("1x1x10").unwrap().extra, 1);
        assert_eq!(Present::new("1x1x10").unwrap().total, 43);
        assert_eq!(Present::new("1x1x10").unwrap().ribbon_for_present, 4); // part 2
        assert_eq!(Present::new("1x1x10").unwrap().ribbon_for_bow, 10); // part 2
        assert_eq!(Present::new("1x1x10").unwrap().total_ribbon, 14); // part 2
    }

    #[test]
    fn test_part1() {
        assert_eq!(part1("2x3x4\n1x1x10"), 101)
    }

    #[test]
    fn test_part2() {
        assert_eq!(part2("2x3x4\n1x1x10"), 48)
    }
}
