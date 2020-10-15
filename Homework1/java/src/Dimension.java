public class Dimension {
  int x;
  int y;
  int area;
  int id;

  Dimension(int x, int y, int id) {
    this.x = x;
    this.y = y;
    this.area = x * y;
    this.id = id;
  }

  public int getArea() {
    return this.area;
  }
}
