import java.util.Scanner;  // Import the Scanner class
import java.io.*;


public class io {
  public static void main(String[] args) {
    Scanner scanner = new Scanner(System.in);
    
    System.out.println("hi whats ur name?");
    
    String name = scanner.nextLine();

    System.out.println("hi " + name + ".");
  }
}
/*
ant compile jar run
*/