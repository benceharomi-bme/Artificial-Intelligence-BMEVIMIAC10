import java.io.BufferedReader;
import java.io.File;
import java.io.FileInputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.PrintStream;
import java.util.ArrayList;
import java.util.Comparator;
import java.util.List;

public class Store {
  Dimension storeDimension;
  int numOfPillars;
  int numOfPallets;
  ArrayList<Position> pillarPositions;
  ArrayList<Dimension> palletDimensions;
  int[][] output;
  int[][] pillarArray;

  public void start(String inputType) throws IOException {
    InputStream inputStream;
    if (inputType.equals(InputType.FILE.toString())) {
      inputStream = new FileInputStream(new File("input.txt"));
    } else {
      inputStream = System.in;
    }
    readInput(inputStream);
    palletDimensions.sort(Comparator.comparing(Dimension::getArea).reversed());
    placePallet(0);
    printOutput();
  }

  public void readInput(InputStream inputStream) throws IOException {
    BufferedReader reader = new BufferedReader(new InputStreamReader(inputStream));
    String[] storeParams = reader.readLine().split("\t");
    storeDimension = new Dimension(Integer.parseInt(storeParams[1]), Integer.parseInt(storeParams[0]), 0);
    numOfPillars = Integer.parseInt(reader.readLine());
    numOfPallets = Integer.parseInt(reader.readLine());
    pillarArray = new int[storeDimension.y][storeDimension.x];
    for (int y = 0; y < storeDimension.y; y++) {
      for (int x = 0; x < storeDimension.x; x++) {
        pillarArray[y][x] = 0;
      }
    }
    pillarPositions = new ArrayList<>(numOfPillars);
    for (int i = 0; i < numOfPillars; i++) {
      String[] pillar = reader.readLine().split("\t");
      pillarArray[Integer.parseInt(pillar[0])][Integer.parseInt(pillar[1])] = 1;
    }
    palletDimensions = new ArrayList<>(numOfPallets);
    for (int i = 0; i < numOfPallets; i++) {
      String[] pallet = reader.readLine().split("\t");
      palletDimensions.add(new Dimension(Integer.parseInt(pallet[1]), Integer.parseInt(pallet[0]), i + 1));
    }
    reader.close();
    output = new int[storeDimension.y][storeDimension.x];
    for (int y = 0; y < storeDimension.y; y++) {
      for (int x = 0; x < storeDimension.x; x++) {
        output[y][x] = 0;
      }
    }
  }

  public void printOutput() {
    PrintStream out = System.out;
    for (int[] row : output) {
      StringBuilder stringBuilder = new StringBuilder();
      int index = 0;
      for (int item : row) {
        stringBuilder.append(item);
        if (row.length - 1 != index)
          stringBuilder.append("\t");
        index++;
      }
      out.println(stringBuilder.toString());
    }
  }

  public void addToArray(Pallet pallet) {
    for (int y = pallet.startY; y < pallet.endY; y++) {
      for (int x = pallet.startX; x < pallet.endX; x++) {
        output[y][x] = pallet.dimension.id;
      }
    }
  }

  public void removeFromArray(Pallet pallet) {
    for (int y = pallet.startY; y < pallet.endY; y++) {
      for (int x = pallet.startX; x < pallet.endX; x++) {
        output[y][x] = 0;
      }
    }
  }

  public boolean checkBorders(Pallet pallet) {
    return !((pallet.endX > storeDimension.x) || (pallet.endY > storeDimension.y));
  }

  public boolean checkPillars(Pallet pallet) {
    for (int y = pallet.startY + 1; y < pallet.endY; y++) {
      for (int x = pallet.startX + 1; x < pallet.endX; x++) {
        if (pillarArray[y][x] != 0) {
          return false;
        }
      }
    }
    return true;
  }

  public boolean checkPallets(Pallet pallet) {
    for (int y = pallet.startY; y < pallet.endY; y++) {
      for (int x = pallet.startX; x < pallet.endX; x++) {
        if (output[y][x] != 0) {
          return false;
        }
      }
    }
    return true;
  }

  public List<Pallet> discoverPossiblePositions(Dimension palletDimension) {
    ArrayList<Pallet> possible = new ArrayList<>();
    for (int y = 0; y < storeDimension.y; y++) {
      for (int x = 0; x < storeDimension.x; x++) {
        if (output[y][x] == 0) {
          Position position = new Position(x, y);
          Pallet pallet = new Pallet(position, palletDimension);
          if (checkBorders(pallet) && checkPillars(pallet) && checkPallets(pallet)) {
            possible.add(pallet);
          }
          Dimension rotated = new Dimension(palletDimension.y, palletDimension.x, palletDimension.id);
          Pallet rotatedPallet = new Pallet(position, rotated);
          if (checkBorders(rotatedPallet) && checkPillars(rotatedPallet) && checkPallets(rotatedPallet)) {
            possible.add(rotatedPallet);
          }
        }
      }
    }
    return possible;
  }

  public boolean placePallet(int i) {
    List<Pallet> possible = discoverPossiblePositions(palletDimensions.get(i));
    if (possible.isEmpty()) {
      return false;
    }
    if (i == palletDimensions.size() - 1) {
      if (!possible.isEmpty()) {
        addToArray(possible.get(0));
        return true;
      } else {
        return false;
      }
    }
    for (Pallet pallet : possible) {
      addToArray(pallet);
      if (placePallet(i + 1)) {
        return true;
      }
      removeFromArray(pallet);
    }
    return false;
  }
}
