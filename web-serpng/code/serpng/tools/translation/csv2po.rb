#!/usr/bin/ruby

# This script processes a .tsv file generated by Google Doc (spreadsheet)'s 
# "Download as plain text" option and outputs a corresponding .po file.
#
# Note: Even though Google Doc says "Download as a plain text (.txt)" file, the
#   actual file downloaded has a ".tsv" extension, and has tab-separated values.
#
# Note: Google Doc should be used instead of Excel because Excel's save-as-tab-
#   separated-values option does not correctly generated UTF-8 encoded data.
#
# Arguments (command-line):
#   A string that denotes the locale name for the .tsv file (e.g., fr_CA).  The script
#   will take as input file the django.tsv file that resides within the locale
#   subdirectory that is associated with the locale name.
# 
# Outputs:
#   A .po file named django.po that is written to the same directory as the
#   .po file.  Any old files named django.po will be renamed to django.po.orig
#

#
# Grab locale name from command line.
#
if ARGV[0].nil?
  puts "Please provide a locale name."
  puts "Usage: csv2po.rb <locale name>"
  puts "Example: csv2po.rb fr_CA"
  exit
else
  locale_name = ARGV[0]
end

#
# Construct both input and output file names.
#
git_dir = %x(git rev-parse --show-toplevel).chomp
csv_file_name = "#{git_dir}/code/serpng/locale/#{locale_name}/LC_MESSAGES/django.tsv"
po_file_name = "#{git_dir}/code/serpng/locale/#{locale_name}/LC_MESSAGES/django.po"

#
# Convert input file to Unix text file.
#
%x(dos2unix -q -c mac #{csv_file_name})

#
# Save a copy of any old "django.po" files.
#
old_po_file_name = po_file_name + ".orig"
%x(mv #{po_file_name} #{old_po_file_name} 2> /dev/null)

#
# Open output file for writing.
#
f_po = File.new(po_file_name, "w")

#
# Delimiters.
#

# Excel spreadsheets can be exported as tab-delimited text files.
$main_delimiter = "\t"

# ' ' separates, within a single Excel column, original file locations.
# (used for reconstructing a .po file from a .csv file)
$file_locations_delimiter = " "

#
# Main
#
File.open(csv_file_name) do |f|
  csv_columns = []
  file_locations_array = []
  f.each do |csv_line|
    csv_columns = csv_line.chomp.split($main_delimiter)

    if csv_columns[0] != "Comments for Translators"  # Throw away column headings.
      # Write file locations.
      file_locations_array = csv_columns[3].split($file_locations_delimiter)
      file_locations_array.each do |file_location|
        f_po.puts "#: " + file_location
      end

      # Write msgid.
      # Note: this simply uses the long concatenated string, even for originally
      # multiline strings.  If compiling this output makes Django barf, then
      # write additional logic to output the original multiline string in Django's
      # multiline string format used in the original .po file.
      f_po.puts "msgid \"" + csv_columns[1] + "\""

      # Write msgstr.
      f_po.puts "msgstr \"" + csv_columns[2] + "\""

      # Write newline to separate translation blocks.
      f_po.puts
    end
  end
end

#
# Close output file.
#
f_po.close