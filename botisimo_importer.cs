using System;
using Microsoft.VisualBasic.FileIO;

public class CPHInline
{
    public bool Execute()
    {
        var path = args[@"filePath"].ToString();
        using (TextFieldParser csvParser = new TextFieldParser(path))
        {
            CPH.LogDebug("Point_Importer: Started");
            csvParser.CommentTokens = new string[]
            {
                "#"
            };
            csvParser.SetDelimiters(new string[] { "," });
            csvParser.HasFieldsEnclosedInQuotes = true;
            // Skip the row with the column names
            csvParser.ReadLine();
            while (!csvParser.EndOfData)
            {
                // Read current line fields, pointer moves to the next line.
                string[] fields = csvParser.ReadFields();
                string user = fields[0];
                string points = fields[1];
                bool pointsimported = CPH.GetUserVar<bool?>(user, "points_imported", true) ?? false;
                int currentpoints = CPH.GetUserVar<int?>("tood", "points", true) ?? -42;
                if (!pointsimported && currentpoints != -42)
                {
                    //CPH.SendMessage(user);
                    int intpoints = Convert.ToInt32(points);
                    CPH.LogDebug("Point_Importer: Imported " + points + " points for " + user);
                    int newpoints = currentpoints + intpoints;
                    CPH.SetUserVar(user, "points", newpoints, true);
                    CPH.SetUserVar(user, "points_imported", true, true);

                }
            }

            CPH.LogDebug("Point_Importer: Completed");
            return true;
        }
    }
}
