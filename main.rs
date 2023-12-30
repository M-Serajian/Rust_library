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


fn main() {
    let original_text = "banana";
    
    // Perform Bidirectional Burrows-Wheeler Transform
    let (bwt_result, original_index) = bwt(original_text);
    println!("Original Text: {}", original_text);
    println!("BWT Result: {}", bwt_result);

    // Perform reverse transformation
    let reversed_text = bbwt(&bwt_result, original_index);
    println!("Reversed Text: {}", reversed_text);
}

fn bbwt(bwt: &str, original_index: usize) -> String {
    let mut table: Vec<Vec<char>> = Vec::new();

    // Initialize the table with empty characters
    for _ in 0..bwt.len() {
        table.push(vec![' '; bwt.len()]);
    }

    // Fill in the table column by column
    for col in 0..bwt.len() {
        let mut column: Vec<(char, usize)> = bwt.chars().enumerate().collect();
        column.sort_by_key(|&(_, idx)| idx);

        for row in 0..bwt.len() {
            table[row][col] = column[row].0;
        }
    }

    // Reconstruct the original string using the table and the original index
    let mut result = String::new();
    let mut current_index = original_index;

    for _ in 0..bwt.len() {
        let c = table[current_index][0];
        result.push(c);
        current_index = table[current_index].iter().position(|&x| x == c).unwrap();
    }

    result
}
