<?php
//j// BOF

/*n// NOTE
----------------------------------------------------------------------------
phpBuilder
Build PHP code for different release targets
----------------------------------------------------------------------------
(C) direct Netware Group - All rights reserved
http://www.direct-netware.de/redirect.php?phpBuilder

This work is distributed under the W3C (R) Software License, but without any
warranty; without even the implied warranty of merchantability or fitness
for a particular purpose.
----------------------------------------------------------------------------
http://www.direct-netware.de/redirect.php?licenses;w3c
----------------------------------------------------------------------------
$Id: php_builder.php,v 1.1 2009/05/11 20:27:09 s4u Exp $
#echo(phpBuilderVersion)#
phpBuilder/#echo(__FILEPATH__)#
----------------------------------------------------------------------------
NOTE_END //n*/
/**
* This is the main PHP "make" worker class file.
*
* @internal   We are using phpDocumentor to automate the documentation process
*             for creating the Developer's Manual. All sections including
*             these special comments will be removed from the release source
*             code.
*             Use the following line to ensure 76 character sizes:
* ----------------------------------------------------------------------------
* @author     direct Netware Group
* @copyright  (C) direct Netware Group - All rights reserved
* @package    ext_core
* @subpackage phpBuilder
* @since      v0.1.00
* @license    http://www.direct-netware.de/redirect.php?licenses;w3c
*             W3C (R) Software License
*/

/* -------------------------------------------------------------------------
All comments will be removed in the "production" packages (they will be in
all development packets)
------------------------------------------------------------------------- */

//j// Functions and classes

/* -------------------------------------------------------------------------
Testing for required classes
------------------------------------------------------------------------- */

$g_continue_check = true;
if (defined ("CLASS_direct_php_builder")) { $g_continue_check = false; }
if (!defined ("CLASS_direct_file")) { $g_continue_check = false; }

if ($g_continue_check)
{
//c// direct_php_builder
/**
* Provides a PHP "make" environment object.
*
* @author     direct Netware Group
* @copyright  (C) direct Netware Group - All rights reserved
* @package    ext_core
* @subpackage phpBuilder
* @since      v0.1.00
* @license    http://www.direct-netware.de/redirect.php?licenses;w3c
*             W3C (R) Software License
*/
class direct_php_builder
{
/**
	* @var mixed $chmod_dirs chmod to set when creating a new directory
*/
	/*#ifndef(PHP4) */protected/* #*//*#ifdef(PHP4):var:#*/ $chmod_dirs;
/**
	* @var mixed $chmod_files chmod to set when creating a new file
*/
	/*#ifndef(PHP4) */protected/* #*//*#ifdef(PHP4):var:#*/ $chmod_files;
/**
	* @var array $debug Debug message container 
*/
	/*#ifndef(PHP4) */public/* #*//*#ifdef(PHP4):var:#*/ $debug;
/**
	* @var boolean $debugging True if we should fill the debug message
	*      container 
*/
	/*#ifndef(PHP4) */protected/* #*//*#ifdef(PHP4):var:#*/ $debugging;
/**
	* @var array $dir_array Directories to be scanned
*/
	/*#ifndef(PHP4) */protected/* #*//*#ifdef(PHP4):var:#*/ $dir_array;
/**
	* @var array $dir_exclude_array Directories to be ignored while scanning
*/
	/*#ifndef(PHP4) */protected/* #*//*#ifdef(PHP4):var:#*/ $dir_exclude_array;
/**
	* @var array $file_array Files to be parsed
*/
	/*#ifndef(PHP4) */protected/* #*//*#ifdef(PHP4):var:#*/ $file_array;
/**
	* @var array $file_exclude_array Files to be ignored while scanning
*/
	/*#ifndef(PHP4) */protected/* #*//*#ifdef(PHP4):var:#*/ $file_exclude_array;
/**
	* @var array $filetype_array Filetype extensions to be parsed
*/
	/*#ifndef(PHP4) */protected/* #*//*#ifdef(PHP4):var:#*/ $filetype_array;
/**
	* @var array $filetype_ascii_array Filetype extensions to be parsed
*/
	/*#ifndef(PHP4) */protected/* #*//*#ifdef(PHP4):var:#*/ $filetype_ascii_array;
/**
	* @var string $output_path Path to generate the output files
*/
	/*#ifndef(PHP4) */protected/* #*//*#ifdef(PHP4):var:#*/ $output_path;
/**
	* @var string $output_strip_prefix Prefix to be stripped from ouput pathes
*/
	/*#ifndef(PHP4) */protected/* #*//*#ifdef(PHP4):var:#*/ $output_strip_prefix;
/**
	* @var integer $time Current UNIX timestamp
*/
	/*#ifndef(PHP4) */protected/* #*//*#ifdef(PHP4):var:#*/ $time;
/**
	* @var integer $timeout_count Retries before timing out
*/
	/*#ifndef(PHP4) */protected/* #*//*#ifdef(PHP4):var:#*/ $timeout_count;
/**
	* @var mixed $umask umask to set before creating a new file
*/
	/*#ifndef(PHP4) */protected/* #*//*#ifdef(PHP4):var:#*/ $umask;

/* -------------------------------------------------------------------------
Construct the class using old and new behavior
------------------------------------------------------------------------- */

	//f// direct_php_builder->__construct () and direct_php_builder->direct_php_builder ()
/**
	* Constructor (PHP5+) __construct (direct_php_builder)
	*
	* @param string $f_include String (delimiter is ",") with directory or file
	*        names to be included.
	* @param string $f_output_path Output path
	* @param string $f_filetype String (delimiter is ",") with extensions of
	*        files to be parsed.
	* @param mixed $f_umask umask to set before creating new directories or
	*        files
	* @param mixed $f_chmod_files chmod to set when creating a new file
	* @param mixed $f_chmod_dirs chmod to set when creating a new directory
	* @param integer $f_time Current UNIX timestamp
	* @param integer $f_timeout_count Retries before timing out
	* @param boolean $f_debug Debug flag
	* @since v0.1.00
*/
	/*#ifndef(PHP4) */public /* #*/function __construct ($f_include,$f_output_path,$f_filetype,$f_umask = NULL,$f_chmod_files = NULL,$f_chmod_dirs = NULL,$f_time = -1,$f_timeout_count = 5,$f_debug = false)
	{
		$this->debugging = $f_debug;

		if ($this->debugging) { $this->debug = array ("phpBuilder/#echo(__FILEPATH__)# -phpBuilder->__construct (direct_php_builder)- (#echo(__LINE__)#)"); }
		$this->chmod_dirs = $f_chmod_dirs;
		$this->chmod_files = $f_chmod_files;
		$this->dir_exclude_array = array ();
		$this->file_exclude_array = array ();
		$this->filetype_ascii_array = array ("txt","js","php","xml");

		if ((strlen ($f_output_path))&&(substr ($f_output_path,-1,1) != "/")) { $f_output_path .= "/"; }
		$this->output_path = $f_output_path;

		$this->output_strip_prefix = "";

		if ($f_time < 0) { $this->time = time (); }
		else { $this->time = $f_time; }

		$this->timeout_count = $f_timeout_count;
		$this->umask = $f_umask;

		$this->filetype_array = array ();
		$f_data_array = explode (",",$f_filetype);
		foreach ($f_data_array as $f_data) { $this->filetype_array[] = $f_data; }

		$this->dir_array = array ();
		$this->file_array = array ();
		$f_data_array = explode (",",$f_include);

		foreach ($f_data_array as $f_data)
		{
			if (is_dir ($f_data)) { $this->dir_array[] = $f_data; }
			elseif (is_file ($f_data)) { $this->file_array[] = $f_data; }
		}
	}
/*#ifdef(PHP4):
/**
	* Constructor (PHP4) direct_php_builder (direct_php_builder)
	*
	* @param mixed $f_umask umask to set before creating a new file
	* @param mixed $f_chmod chmod to set when creating a new file
	* @param integer $f_time Current UNIX timestamp
	* @param integer $f_timeout_count Retries before timing out
	* @param boolean $f_debug Debug flag
	* @since v0.1.00
*\/
	function direct_php_builder ($f_include,$f_output_path,$f_filetype,$f_umask = NULL,$f_chmod = NULL,$f_time = -1,$f_timeout_count = 5,$f_debug = false) { $this->__construct ($f_include,$f_output_path,$f_filetype,$f_umask,$f_chmod,$f_time,$f_timeout_count,$f_debug); }
:#\n*/
	//f// direct_php_builder->__destruct ()
/**
	* Destructor (PHP5+) __destruct (direct_php_builder)
	*
	* @since v0.1.00
*/
	/*#ifndef(PHP4) */public /* #*/function __destruct ()
	{
		// Nothing to do for me
	}

	//f// direct_php_builder->condition_parse ($f_condition_array)
/**
	* Parse the given condition and returns the corresponding result.
	*
	* @param  array $f_condition_array Condition array
	* @return boolean True if condition is met
	* @since  v0.1.00
*/
	/*#ifndef(PHP4) */protected /* #*/function condition_parse ($f_condition_array)
	{
		if ($this->debugging) { $this->debug[] = "phpBuilder/#echo(__FILEPATH__)# -phpBuilder->condition_parse (+f_condition_array)- (#echo(__LINE__)#)"; }
		$f_return = false;

		if (count ($f_condition_array) == 3)
		{
			$f_value = $this->get_variable ($f_condition_array[2]);

			switch ($f_condition_array[1])
			{
			case "ifdef":
			{
				if ($f_value != NULL) { $f_return = true; }
				break 1;
			}
			case "ifndef":
			{
				if ($f_value == NULL) { $f_return = true; }
				break 1;
			}
			}
		}

		return $f_return;
	}

	//f// direct_php_builder->add_filetype_ascii ($f_extension)
/**
	* Adds an extension to the list of ASCII file types.
	*
	* @param  string $f_extension File type extension to add
	* @since  v0.1.01
*/
	/*#ifndef(PHP4) */public /* #*/function add_filetype_ascii ($f_extension)
	{
		if ($this->debugging) { $this->debug[] = "phpBuilder/#echo(__FILEPATH__)# -phpBuilder->add_filetype_ascii ($f_extension)- (#echo(__LINE__)#)"; }
		$this->filetype_ascii_array[] = $f_extension;
	}

	//f// direct_php_builder->data_parse ($f_data,$f_file_path,$f_file_name)
/**
	* Parse the given content and return a line based array.
	*
	* @param  string $f_data Data to be parsed
	* @param  string $f_file_path File path
	* @param  string $f_file_name File name
	* @uses   direct_php_builder::data_parse_walker()
	* @return mixed Line based array; False on error
	* @since  v0.1.00
*/
	/*#ifndef(PHP4) */protected /* #*/function data_parse ($f_data,$f_file_path,$f_file_name)
	{
		if ($this->debugging) { $this->debug[] = "phpBuilder/#echo(__FILEPATH__)# -phpBuilder->data_parse (+f_data)- (#echo(__LINE__)#)"; }
		$f_return = false;

		$f_data = str_replace (array ("#echo(__FILE__)#","#echo(__FILEPATH__)#"),(array ($f_file_name,$f_file_path)),($this->data_parse_walker ($f_data)));

		if (preg_match_all ("/#echo\(((?!_)\w+)\)#/",$f_data,$f_result_array,PREG_PATTERN_ORDER))
		{
			$f_match_counter = 0;
			$f_matched_array = array ();

			foreach ($f_result_array[0] as $f_result)
			{
				if (!isset ($f_matched_array[$f_result]))
				{
					$f_value = $this->get_variable ($f_result_array[1][$f_match_counter]);

					if ($f_value == NULL) { $f_data = str_replace ($f_result,$f_result_array[1][$f_match_counter],$f_data); }
					else { $f_data = str_replace ($f_result,$f_value,$f_data); }

					$f_matched_array[$f_result] = $f_result_array[1][$f_match_counter];
				}

				$f_match_counter++;
			}
		}

		$f_return = preg_split ("#(\r\n|\r|\n)#",$f_data);

		if (strpos ($f_data,"#echo(__LINE__)#") !== false)
		{
			foreach ($f_return as $f_line => $f_data) { $f_return[$f_line] = str_replace ("#echo(__LINE__)#",$f_line,$f_data); }
		}

		return $f_return;
	}

	//f// direct_php_builder->data_parse_walker ($f_data,$f_zone_valid = false,$f_zone_tag = "")
/**
	* Parse the given content part recursively and returns the result.
	*
	* @param  string $f_data Input data
	* @param  boolean $f_zone_valid True if the zone condition resulted in false
	* @param  string $f_zone_tag Zone end tag
	* @uses   direct_php_builder::condition_parse()
	* @uses   direct_php_builder::data_parse_walker()
	* @return string Parsed content part
	* @since  v0.1.00
*/
	/*#ifndef(PHP4) */protected /* #*/function data_parse_walker ($f_data,$f_zone_valid = false,$f_zone_tag = "")
	{
		if ($this->debugging) { $this->debug[] = "phpBuilder/#echo(__FILEPATH__)# -phpBuilder->data_parse_walker (+f_data,+f_zone_valid,$f_zone_tag)- (#echo(__LINE__)#)"; }
		$f_return = "";

		if ($f_zone_tag) { $f_sub = true; }
		else { $f_sub = false; }

		$f_command_array = array ();
		$f_command_false_positive = false;
		$f_data_array = preg_split ("/(\/\*#\w+\(\w+\))/",$f_data,2,PREG_SPLIT_DELIM_CAPTURE);
		$f_data_pointer = 0;

		while (isset ($f_data_array[$f_data_pointer]))
		{
			if (preg_match ("/^\/\*#(\w+)\((\w+)\)$/",$f_data_array[$f_data_pointer],$f_command_array)) { $f_data_pointer++; }

			if (isset ($f_data_array[$f_data_pointer]))
			{
				if (empty ($f_command_array))
				{
					if ($f_sub)
					{
						$f_data_sub_array = explode ($f_zone_tag,$f_data_array[$f_data_pointer],2);

						if (count ($f_data_sub_array) == 2)
						{
							$f_data_sub_length = strlen ($f_data_sub_array[1]);

							if (($f_data_sub_length > 1)&&(substr ($f_data_sub_array[1],0,2) == "*/"))
							{
								if ($f_zone_valid) { $f_return .= str_replace ("*\/","*/",$f_data_sub_array[0]); }
								$f_return .= substr ($f_data_sub_array[1],2);
							}
							elseif (($f_data_sub_length > 3)&&(substr ($f_data_sub_array[1],0,4) == "\\n*/"))
							{
								if ($f_zone_valid) { $f_return .= str_replace ("*\/","*/",$f_data_sub_array[0]); }
								$f_return .= preg_replace ("#^(\r\n|\r|\n)#","",(substr ($f_data_sub_array[1],4)));
							}
							else { $f_command_false_positive = true; }
						}
						else { $f_command_false_positive = true; }
					}
					else { $f_return .= $f_data_array[$f_data_pointer]; }
				}
				else
				{
					if (preg_match ("#^\:(\r\n|\r|\n)(.*?)$#s",$f_data_array[$f_data_pointer],$f_result_array))
					{
						if (($f_command_array[1] == "ifdef")||($f_command_array[1] == "ifndef")) { $f_return .= $this->data_parse_walker ($f_result_array[2],($this->condition_parse ($f_command_array)),":#"); }
						else { $f_command_false_positive = true; }
					}
					elseif ($f_data_array[$f_data_pointer][0] == ":")
					{
						if (($f_command_array[1] == "ifdef")||($f_command_array[1] == "ifndef")) { $f_return .= $this->data_parse_walker (substr ($f_data_array[$f_data_pointer],1),($this->condition_parse ($f_command_array)),":#"); }
						else { $f_command_false_positive = true; }
					}
					elseif (substr ($f_data_array[$f_data_pointer],0,3) == "#*/")
					{
						if ($f_command_array[1] == "echo")
						{
							switch ($f_command_array[2])
							{
							case "__FILE__":
							{
								$f_return .= $f_file_name;
								break 1;
							}
							case "__FILEPATH__":
							{
								$f_return .= $f_file_path;
								break 1;
							}
							case "__LINE__": { break 1; }
							default:
							{
								$f_value = $this->get_variable ($f_command_array[2]);

								if ($f_value == NULL) { $f_return .= $f_command_array[2]; }
								else { $f_return .= $f_value; }
							}
							}

							$f_return .= substr ($f_data_array[$f_data_pointer],3);
						}
						else { $f_command_false_positive = true; }
					}
					elseif (preg_match ("/^[ ]\*\/(\r\n|\r|\n)(.*?)$/s",$f_data_array[$f_data_pointer],$f_result_array))
					{
						if (($f_command_array[1] == "ifdef")||($f_command_array[1] == "ifndef")) { $f_return .= $this->data_parse_walker ($f_result_array[2],($this->condition_parse ($f_command_array)),"/* #"); }
						else { $f_command_false_positive = true; }
					}
					elseif (substr ($f_data_array[$f_data_pointer],0,3) == " */")
					{
						if (($f_command_array[1] == "ifdef")||($f_command_array[1] == "ifndef")) { $f_return .= $this->data_parse_walker (substr ($f_data_array[$f_data_pointer],3),($this->condition_parse ($f_command_array)),"/* #"); }
						else { $f_command_false_positive = true; }
					}
					else { $f_command_false_positive = true; }
					
					if ($f_command_false_positive) { $f_return .= $f_command_array[0]; }
					$f_command_array = array ();
				}

				if ($f_command_false_positive)
				{
					$f_return .= $f_data_array[$f_data_pointer];
					$f_command_false_positive = false;
				}
			}
			else { $f_return .= $f_command_array[0]; }

			$f_data_pointer++;
		}

		return $f_return;
	}

	//f// direct_php_builder->dir_create ($f_dir_path,$f_timeout = -1)
/**
	* Creates a directory (or returns the status of is_writable if it exists).
	* Use slashes - even on Microsoft(R) Windows(R) machines.
	*
	* @param  string $f_dir_path Path to the new directory.
	* @param  integer $f_timeout Timeout to use
	* @uses   direct_php_builder::dir_create()
	* @return boolean True on success
	* @since  v0.1.00
*/
	/*#ifndef(PHP4) */protected /* #*/function dir_create ($f_dir_path,$f_timeout = -1)
	{
		if ($this->debugging) { $this->debug[] = "phpBuilder/#echo(__FILEPATH__)# -phpBuilder->dir_create ($f_dir_path,$f_timeout)- (#echo(__LINE__)#)"; }

		$f_dir_path = preg_replace ("#\/$#","",$f_dir_path);

		if ((!strlen ($f_dir_path))||($f_dir_path == ".")) { $f_return = false; }
		elseif ((is_dir ($f_dir_path))&&(is_writable ($f_dir_path))) { $f_return = true; }
		elseif (file_exists ($f_dir_path)) { $f_return = false; }
		else
		{
			$f_continue_check = true;
			$f_return = false;

			if ($f_timeout < 0) { $f_timeout_time = ($this->time + $this->timeout_count); }
			else { $f_timeout_time = ($this->time + $f_timeout); }

			$f_dir_array = explode ("/",$f_dir_path);
			$f_dir_count = count ($f_dir_array);

			if ($f_dir_count > 1)
			{
				array_pop ($f_dir_array);
				$f_dir_basepath = implode ("/",$f_dir_array);
				$f_continue_check = $this->dir_create ($f_dir_basepath);
			}

			if (($f_continue_check)&&($f_timeout_time > (time ())))
			{
				if ($this->umask) { umask (intval ($this->umask,8)); }

				if (isset ($this->chmod_dirs)) { $f_chmod = intval ($this->chmod_dirs,8); }
				else { $f_chmod = 0750; }

				if (@mkdir ($f_dir_path,$f_chmod)) { $f_return = is_writable ($f_dir_path); }
			}
		}

		return $f_return;
	}

	//f// direct_php_builder->file_parse ($f_file_path)
/**
	* Handle the given file and call the content parse method.
	*
	* @param  string $f_file_path Path to the requested file
	* @uses   direct_php_builder::data_parse()
	* @uses   direct_php_builder::file_write()
	* @return boolean True on success
	* @since  v0.1.00
*/
	/*#ifndef(PHP4) */protected /* #*/function file_parse ($f_file_path)
	{
		if ($this->debugging) { $this->debug[] = "phpBuilder/#echo(__FILEPATH__)# -phpBuilder->file_parse ($f_file_path)- (#echo(__LINE__)#)"; }
		$f_return = false;

		$f_file_array = pathinfo ($f_file_path);
		$f_file_object = new direct_file ($this->umask,$this->chmod_files,$this->time,$this->timeout_count,$this-debugging);
		$f_file_text_mode = false;

		if ((isset ($f_file_array['extension']))&&(in_array ($f_file_array['extension'],$this->filetype_ascii_array))) { $f_file_text_mode = true; }
		elseif (isset ($f_file_array['basename'])) { $f_file_text_mode = in_array ($f_file_array['basename'],$this->filetype_ascii_array); }

		if ((($f_file_text_mode)&&($f_file_object->open ($f_file_path,true,"r")))||($f_file_object->open ($f_file_path,true,"rb")))
		{
			$f_file_content = $f_file_object->read ();
			$f_file_object->close ();
		}
		else { $f_file_content =  NULL; }

		$f_file_path = preg_replace ("#^".(preg_quote ($this->output_strip_prefix))."#","",$f_file_path);

		if (($f_file_text_mode)&&(is_string ($f_file_content)))
		{
			$f_file_array = $this->data_parse ($f_file_content,$f_file_path,$f_file_array['basename']);

			if (strpos ($f_file_content,"\r\n") !== false) { $f_file_content = "\r\n"; }
			elseif (strpos ($f_file_content,"\r") !== false) { $f_file_content = "\r"; }
			else { $f_file_content = "\n"; }

			if (is_array ($f_file_array)) { $f_return = $this->file_write (implode ($f_file_content,$f_file_array),$this->output_path.$f_file_path,"w+"); }
		}
		else { $f_return = $this->file_write ($f_file_content,$this->output_path.$f_file_path); }

		return $f_return;
	}

	//f// direct_php_builder->file_write ($f_file_content,$f_file_path,$f_file_mode = "w+b")
/**
	* Write the given file to the defined location. Create subdirectories if
	* needed.
	*
	* @param  string $f_file_content Parsed content
	* @param  string $f_file_path Path to the output file
	* @param  string $f_file_mode Filemode to use
	* @uses   direct_php_builder::dir_create()
	* @return boolean True on success
	* @since  v0.1.00
*/
	/*#ifndef(PHP4) */protected /* #*/function file_write ($f_file_content,$f_file_path,$f_file_mode = "w+b")
	{
		if ($this->debugging) { $this->debug[] = "phpBuilder/#echo(__FILEPATH__)# -phpBuilder->file_write (+f_file_content,$f_file_path,$f_file_mode)- (#echo(__LINE__)#)"; }
		$f_return = false;

		$f_file_array = pathinfo ($f_file_path);

		if ((!isset ($f_file_array['dirname']))||($this->dir_create ($f_file_array['dirname'])))
		{
			$f_file_object = new direct_file ($this->umask,$this->chmod_files,$this->time,$this->timeout_count,$this-debugging);

			if ($f_file_object->open ($f_file_path,false,$f_file_mode))
			{
				$f_return = $f_file_object->write ($f_file_content);
				$f_file_object->close ();
			}
		}

		return $f_return;
	}

	//f// direct_php_builder->get_variable ($f_name)
/**
	* Gets the variable content with the given name.
	*
	* @param  string $f_name Variable name
	* @return mixed Variable content; NULL if undefined
	* @since  v0.1.01
*/
	/*#ifndef(PHP4) */protected /* #*/function get_variable ($f_name)
	{
		if ($this->debugging) { $this->debug[] = "phpBuilder/#echo(__FILEPATH__)# -phpBuilder->get_variable ($f_name)- (#echo(__LINE__)#)"; }
		return constant ($f_name);
	}

	//f// direct_php_builder->make_all ()
/**
	* Parse and rewrite all directories and files given as include definitions.
	*
	* @uses   direct_php_builder::file_parse()
	* @uses   direct_php_builder::workdir_scan()
	* @return boolean True on success
	* @since  v0.1.00
*/
	/*#ifndef(PHP4) */public /* #*/function make_all ()
	{
		if ($this->debugging) { $this->debug[] = "phpBuilder/#echo(__FILEPATH__)# -phpBuilder->make_all ()- (#echo(__LINE__)#)"; }
		$f_return = false;

		if ((!empty ($this->dir_array))&&(!empty ($this->filetype_array))) { $this->workdir_scan (); }

		if (empty ($this->file_array)) { trigger_error ("phpBuilder/#echo(__FILEPATH__)# -phpBuilder->make_all ()- (#echo(__LINE__)#) reports: No valid files found for parsing",E_USER_ERROR); }
		else
		{
			foreach ($this->file_array as $f_file)
			{
				echo "\n>> Parsing $f_file ... ";

				if ($this->file_parse ($f_file)) { echo "done"; }
				else { echo "failed"; }
			}
		}

		return $f_return;
	}

	//f// direct_php_builder->set_exclude ($f_exclude)
/**
	* Add "exclude" definitions for directories and files.
	*
	* @param  string $f_exclude String (delimiter is ",") with exclude names or pathes
	* @since  v0.1.00
*/
	/*#ifndef(PHP4) */public /* #*/function set_exclude ($f_exclude)
	{
		if ($this->debugging) { $this->debug[] = "phpBuilder/#echo(__FILEPATH__)# -phpBuilder->set_exclude ($f_exclude)- (#echo(__LINE__)#)"; }

		if (is_string ($f_exclude))
		{
			$f_exclude_array = explode (",",$f_exclude);

			foreach ($f_exclude_array as $f_exclude_array)
			{
				$this->dir_exclude_array[] = $f_exclude_array;
				$this->file_exclude_array[] = $f_exclude_array;
			}
		}
		else { trigger_error ("phpBuilder/#echo(__FILEPATH__)# -phpBuilder->set_exclude ()- (#echo(__LINE__)#) reports: Given parameter is not a string",E_USER_NOTICE); }
	}

	//f// direct_php_builder->set_exclude_dirs ($f_exclude)
/**
	* Add "exclude" definitions for directories.
	*
	* @param  string $f_exclude String (delimiter is ",") with exclude names or
	*         pathes
	* @since  v0.1.00
*/
	/*#ifndef(PHP4) */public /* #*/function set_exclude_dirs ($f_exclude)
	{
		if ($this->debugging) { $this->debug[] = "phpBuilder/#echo(__FILEPATH__)# -phpBuilder->set_exclude_dirs ($f_exclude)- (#echo(__LINE__)#)"; }

		if (is_string ($f_exclude))
		{
			$f_exclude_array = explode (",",$f_exclude);
			foreach ($f_exclude_array as $f_exclude_array) { $this->dir_exclude_array[] = $f_exclude_array; }
		}
		else { trigger_error ("phpBuilder/#echo(__FILEPATH__)# -phpBuilder->set_exclude_dirs ()- (#echo(__LINE__)#) reports: Given parameter is not a string",E_USER_NOTICE); }
	}

	//f// direct_php_builder->set_exclude_files ($f_exclude)
/**
	* Add "exclude" definitions for files.
	*
	* @param  string $f_exclude String (delimiter is ",") with exclude names or
	*         pathes
	* @since  v0.1.00
*/
	/*#ifndef(PHP4) */public /* #*/function set_exclude_files ($f_exclude)
	{
		if ($this->debugging) { $this->debug[] = "phpBuilder/#echo(__FILEPATH__)# -phpBuilder->set_exclude_files ($f_exclude)- (#echo(__LINE__)#)"; }

		if (is_string ($f_exclude))
		{
			$f_exclude_array = explode (",",$f_exclude);
			foreach ($f_exclude_array as $f_exclude_array) { $this->file_exclude_array[] = $f_exclude_array; }
		}
		else { trigger_error ("phpBuilder/#echo(__FILEPATH__)# -phpBuilder->set_exclude_files ()- (#echo(__LINE__)#) reports: Given parameter is not a string",E_USER_NOTICE); }
	}

	//f// direct_php_builder->set_strip_prefix ($f_strip_prefix)
/**
	* Define a prefix to be stripped from output pathes.
	*
	* @param  string $f_strip_prefix Prefix definition
	* @since  v0.1.00
*/
	/*#ifndef(PHP4) */public /* #*/function set_strip_prefix ($f_strip_prefix)
	{
		if ($this->debugging) { $this->debug[] = "phpBuilder/#echo(__FILEPATH__)# -phpBuilder->set_strip_prefix ($f_strip_prefix)- (#echo(__LINE__)#)"; }

		if (is_string ($f_strip_prefix)) { $this->output_strip_prefix = $f_strip_prefix; }
		else { trigger_error ("phpBuilder/#echo(__FILEPATH__)# -phpBuilder->set_strip_prefix ()- (#echo(__LINE__)#) reports: Given parameter is not a string",E_USER_NOTICE); }
	}

	//f// direct_php_builder->workdir_scan ()
/**
	* Scan given directories for files to be parsed.
	*
	* @since v0.1.00
*/
	/*#ifndef(PHP4) */protected /* #*/function workdir_scan ()
	{
		if ($this->debugging) { $this->debug[] = "phpBuilder/#echo(__FILEPATH__)# -phpBuilder->workdir_scan ()- (#echo(__LINE__)#)"; }

		$f_strip_prefix = preg_quote ($this->output_strip_prefix);
/* -------------------------------------------------------------------------
Create a list of files - we need to scan directories recursively ...
------------------------------------------------------------------------- */

		echo "\n> Ready to build file index";
		$f_dir_counter = 0;

		do
		{
			echo "\n>> Scanning {$this->dir_array[$f_dir_counter]} ... ";

			if ((is_dir ($this->dir_array[$f_dir_counter]))&&(is_readable ($this->dir_array[$f_dir_counter])))
			{
				$f_content_array = scandir ($this->dir_array[$f_dir_counter]);

				foreach ($f_content_array as $f_content)
				{
					if ($f_content[0] != ".")
					{
						if (substr ($this->dir_array[$f_dir_counter],-1,1) == "/") { $f_content_extended = $this->dir_array[$f_dir_counter].$f_content; }
						else { $f_content_extended = $this->dir_array[$f_dir_counter]."/".$f_content; }

						$f_content_estripped = preg_replace ("#^$f_strip_prefix#","",$f_content_extended);

						if (is_dir ($f_content_extended))
						{
							if ((!in_array ($f_content,$this->dir_exclude_array))&&(!in_array ($f_content_estripped,$this->dir_exclude_array))) { $this->dir_array[] = $f_content_extended; }
						}
						elseif (is_file ($f_content_extended))
						{
							$f_content_array = pathinfo ($f_content);
							$f_content_id = md5 ($f_content_estripped);

							if ((isset ($f_content_array['extension']))&&(in_array ($f_content_array['extension'],$this->filetype_array))&&(!in_array ($f_content,$this->file_exclude_array))&&(!in_array ($f_content_estripped,$this->file_exclude_array))) { $this->file_array[$f_content_id] = $f_content_extended; }
						}
					}
				}

				echo "done";
			}
			else { echo "failed"; }

			$f_dir_counter++;
		}
		while (isset ($this->dir_array[$f_dir_counter]));
	}
}

/* -------------------------------------------------------------------------
Define this class
------------------------------------------------------------------------- */

define ("CLASS_direct_php_builder",true);
}

//j// EOF
?>