import java.io.IOException;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.Reducer;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;

public class MovieRatingSorterMR {
    public static class MovieRatingMapper extends Mapper<Object, Text, Text, Text> {
        private Text userId = new Text();
        private Text movieRating = new Text();

        public void map(Object key, Text value, Context context) throws IOException, InterruptedException {
            String[] fields = value.toString().split(",");
            if (fields.length == 4) {
                userId.set(fields[1]);
                movieRating.set(fields[0] + "," + fields[2]);
                context.write(userId, movieRating);
            }
        }
    }

    public static class MovieRatingReducer extends Reducer<Text, Text, Text, Text> {
        private Text result = new Text();

        public void reduce(Text key, Iterable<Text> values, Context context) throws IOException, InterruptedException {
            List<String> ratings = new ArrayList<>();
            for (Text value : values) {
                ratings.add(value.toString());
            }
            Collections.sort(ratings);

            StringBuilder output = new StringBuilder("[");
            for (int i = 0; i < ratings.size(); i++) {
                if (i > 0) {
                    output.append(",");
                }
                output.append("[").append(ratings.get(i)).append("]");
            }
            output.append("]");
            result.set(output.toString());

            context.write(key, result);
        }
    }

    public static void main(String[] args) throws Exception {
        Configuration conf = new Configuration();
        Job job = Job.getInstance(conf, "Movie Rating Sorter");

        job.setJarByClass(MovieRatingSorterMR.class);
        job.setMapperClass(MovieRatingMapper.class);
        job.setReducerClass(MovieRatingReducer.class);

        job.setOutputKeyClass(Text.class);
        job.setOutputValueClass(Text.class);

        FileInputFormat.addInputPath(job, new Path(args[0]));
        FileOutputFormat.setOutputPath(job, new Path(args[1]));

        System.exit(job.waitForCompletion(true) ? 0 : 1);
    }
}
