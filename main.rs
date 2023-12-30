use std::io;

fn main() {
    // Prompt the user for input
    println!("Enter your name:");

    // Create a mutable String to store the user's input
    let mut input = String::new();

    // Read the user's input from the console
    io::stdin().read_line(&mut input)
        .expect("Failed to read line");

    // Trim any leading or trailing whitespace from the input
    let trimmed_input = input.trim();

    // Print a personalized greeting
    println!("Hello, {}! Welcome to the world of Rust!", trimmed_input);
}
