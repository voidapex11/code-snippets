package voidapex11;
import java.util.Scanner;  // Import the Scanner class
import java.io.*;


public class main {
  public static void main(String[] args) {
    Scanner scanner = new Scanner(System.in);
    String correctAnswer = "yes";
    System.out.println("do you like java");
    String answerGiven = scanner.nextLine();
    // it must be .equals for some reason
    if (answerGiven.equals(correctAnswer)) {
      System.out.println("good");
    } else {
      System.out.println("u suck");
    }
  }
}