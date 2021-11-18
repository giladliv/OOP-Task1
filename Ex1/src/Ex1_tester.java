import ex1.Ex1_main;

public class Ex1_tester
{
    public static void main(String[] args)
    {
        if (args==null || args.length<4) {
            args = new String[4];
            args[0] = "206768962,316320282";
            args[1] = "data/Ex1_input/Ex1_Buildings/B5.json";
            args[2] = "data/Ex1_output/Ex1_Calls_case_1_a.csv";
            long time = System.currentTimeMillis();
            args[3] = "out/logs/Ex1_report_case_5_d" + "_" + time + "_ID_.log";
        }
        Ex1_main.main(args);
    }
}
