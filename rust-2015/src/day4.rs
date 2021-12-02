/*
--- Day 4: The Ideal Stocking Stuffer ---

Santa needs help mining some AdventCoins (very similar to bitcoins) to use as gifts for all the economically forward-thinking little girls and boys.

To do this, he needs to find MD5 hashes which, in hexadecimal, start with at least five zeroes. The input to the MD5 hash is some secret key (your puzzle input, given below) followed by a number in decimal. To mine AdventCoins, you must find Santa the lowest positive number (no leading zeroes: 1, 2, 3, ...) that produces such a hash.

For example:

    If your secret key is abcdef, the answer is 609043, because the MD5 hash of abcdef609043 starts with five zeroes (000001dbbfa...), and it is the lowest such number to do so.
    If your secret key is pqrstuv, the lowest number it combines with to make an MD5 hash starting with five zeroes is 1048970; that is, the MD5 hash of pqrstuv1048970 looks like 000006136ef....

--- Part Two ---

Now find one that starts with six zeroes.
*/

extern crate crypto;

use crypto::digest::Digest;
use crypto::md5::Md5;

fn is_md5_hash_with_five_leading_zeroes(md5hash: &[u8]) -> bool {
    return md5hash[0] as u32 + md5hash[1] as u32 + (md5hash[2] >> 4) as u32 == 0;
}

fn is_md5_hash_with_six_leading_zeroes(md5hash: &[u8]) -> bool {
    return md5hash[0] as u32 + md5hash[1] as u32 + md5hash[2] as u32 == 0;
}

fn find_md5_hash(
    hasher: &mut Md5,
    secret_key: &str,
    number: u32,
    condition: &dyn Fn(&[u8]) -> bool,
) -> Result<bool, String> {
    // Reference: https://gist.github.com/gkbrk/2e4835e3a17b3fb6e1e7
    let key_bytes = secret_key.as_bytes();

    hasher.input(key_bytes);
    hasher.input(number.to_string().as_bytes());

    let mut output = [0; 16]; // An MD5 hash is 16 bytes
    hasher.result(&mut output);
    hasher.reset();

    Ok(condition(&output))
}

pub fn part1(input: &str) -> Result<u32, &str> {
    let mut hasher = Md5::new();

    for i in 0..std::u32::MAX {
        if find_md5_hash(
            &mut hasher,
            &input,
            i,
            &is_md5_hash_with_five_leading_zeroes,
        )
        .unwrap()
        {
            return Ok(i);
        }
    }

    Err("Could not find hash with 5 leading zeroes")
}

pub fn part2(input: &str) -> Result<u32, &str> {
    let mut hasher = Md5::new();

    for i in 0..std::u32::MAX {
        if find_md5_hash(&mut hasher, &input, i, &is_md5_hash_with_six_leading_zeroes).unwrap() {
            return Ok(i);
        }
    }

    Err("Could not find hash with 6 leading zeroes")
}

#[cfg(test)]
mod tests {
    use crate::day4::{find_md5_hash, is_md5_hash_with_five_leading_zeroes};
    use crypto::md5::Md5;
    use hex::FromHex;

    #[test]
    fn test_is_md5_hash_with_five_leading_zeroes() {
        let md5hash: Vec<u8> = Vec::from_hex("000001dbbfa3a5c83a2d506429c7b00e").unwrap();
        assert_eq!(is_md5_hash_with_five_leading_zeroes(&md5hash), true);
    }

    #[test]
    fn test_part1() {
        let mut hasher = Md5::new();
        assert_eq!(
            find_md5_hash(
                &mut hasher,
                "abcdef",
                609043,
                &is_md5_hash_with_five_leading_zeroes
            )
            .unwrap(),
            true
        );
    }
}
