fn bwt(text: &str) -> (String, usize) {
    let mut rotations: Vec<String> = Vec::new();

    // Generate all rotations of the input string
    for i in 0..text.len() {
        let rotation = format!("{}{}", &text[i..], &text[..i]);
        rotations.push(rotation);
    }

    // Sort the rotations lexicographically
    rotations.sort();

    // Extract the last characters of each rotation to form the BWT result
    let bwt: String = rotations.iter().map(|s| s.chars().last().unwrap()).collect();

    // Find the index of the original string in the sorted rotations
    let original_index = rotations.iter().position(|s| *s == text).unwrap();

    (bwt, original_index)
}