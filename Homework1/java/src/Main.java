import java.io.IOException;

public class Main {

    public static void main(String[] args) {
        String arg = (args.length > 0) ? args[0] : "";
        Store store = new Store();
        try {
            store.start(arg);
        } catch (IOException ex) {
            System.out.println(ex);
        }
    }
}