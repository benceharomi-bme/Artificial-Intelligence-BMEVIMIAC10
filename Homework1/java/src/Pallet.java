public class Pallet {
  Position position;
  Dimension dimension;
  int startX;
  int endX;
  int startY;
  int endY;

  Pallet(Position position, Dimension dimension){
    this.position = position;
    this.dimension = dimension;
    this.startX = position.x;
    this.endX = position.x+dimension.x;
    this.startY = position.y;
    this.endY = position.y + dimension.y;
  }
}
