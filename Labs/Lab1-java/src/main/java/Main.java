import java.util.List;
import java.util.Scanner;

public class Main {

  public static double getCoefficient(String prompt) {
    Scanner scanner = new Scanner(System.in);
    double coef;
    while (true) {
      System.out.print(prompt);
      String input = scanner.nextLine();
      try {
        coef = Double.parseDouble(input);
        break;
      } catch (NumberFormatException e) {
        System.out.println("Некорректное значение. Пожалуйста, введите действительное число.");
      }
    }
    return coef;
  }

  public static void main(String[] args) {

    double a = 0, b = 0, c = 0;

    if (args.length != 0) {
      try {
        a = Double.parseDouble(args[0]);
        b = Double.parseDouble(args[1]);
        c = Double.parseDouble(args[2]);
      } catch (NumberFormatException e) {
        System.out.println("Ошибка ввода");
      }
    } else {
      a = getCoefficient("Введите коэффициент A: ");
      b = getCoefficient("Введите коэффициент B: ");
      c = getCoefficient("Введите коэффициент C: ");
    }

    BiquadraticEquation equation = new BiquadraticEquation(a, b, c);
    List<Double> roots = equation.getRoots();

    if (roots.isEmpty()) {
      System.out.println("Нет действительных корней.");
    } else {
      System.out.println("Найденные корни:");
      for (double root : roots) {
        System.out.println(root);
      }
    }
  }
}
